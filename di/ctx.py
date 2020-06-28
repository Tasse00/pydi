import inspect
import json
import logging
from inspect import _empty
from typing import Optional, Dict, List, Any, Union
import xml.dom.minidom

from di.bean import Bean, Property, PropertyType
from di.decorator import get_collected_group
from di.ref import Ref, ClsRef, RefType, IdRef
from di.utils import get_cls_name, get_cls_from_name


class Context:

    def __init__(self):
        self.id_map: Dict[str, Bean] = {}
        self.cls_map: Dict[str, List[Bean]] = {}
        self.singleton_cache: Dict[str, Any] = {} # {id: instance}
        self.logger = logging.getLogger(__name__ + "-" + str(id(self))[:4])

    def get_beans(self) -> List[Bean]:
        return list(self.id_map.values())

    def format_beans_xml(self, **kwargs):
        doc = xml.dom.minidom.Document()
        beans_elem = doc.createElement('beans')
        for bean in self.get_beans():
            beans_elem.appendChild(bean.to_xml())
        doc.appendChild(beans_elem)
        return doc.toprettyxml(**kwargs)

    def build_params(self, cls: type, refs: Dict[str, Ref], consts: Dict[str, Any]) -> List[Property]:
        """
        直接注册Bean时，构造Bean的Params. 若所给参数不满足目标类初始化条件，则抛出异常

        1. 引用Refs及常量Consts两定义中不可同时对同一参数进行定义
        2. 不在Refs及Consts中的参数，优先以默认值补充至为Consts定义中
        3. 不在Refs及Consts中的参数，且不存在默认值，则以ClsRef形式补充至Consts定义中
        4. 存在不在Refs及Consts中的参数，且不存在默认值并未基本类型的参数，直接抛出异常
        """

        # 校验refs及consts是否存在冲突项
        repeated_params = set(refs.keys()).intersection(set(consts.keys()))
        if len(repeated_params) > 0:
            raise ValueError("duplicated params {} for cls {}".format(
                repeated_params, get_cls_name(cls)
            ))

        # 构造每个参数的Ref
        def_params = list(inspect.signature(cls).parameters.values())
        params: List[Property] = []
        for dp in def_params:
            if dp.name in consts:  # 指定常量
                params.append(Property(
                    name=dp.name,
                    type=PropertyType.Const,
                    value=consts[dp.name]
                ))
            elif dp.name in refs:  # 指定引用
                params.append(Property(
                    name=dp.name,
                    type=PropertyType.Ref,
                    value=refs[dp.name]
                ))
            else:  # 默认处理逻辑
                if dp.default is not _empty:  # 优先使用默认参数
                    params.append(Property(name=dp.name, type=PropertyType.Const, value=dp.default))
                else:
                    if dp.annotation in (int, float, str, list, set, dict, tuple):
                        raise ValueError("Basic type params must have default value or defined in consts.")
                    else:
                        params.append(Property(name=dp.name, type=PropertyType.Ref, value=ClsRef(dp.annotation)))

        return params

    def find_bean_by_ref(self, ref: Ref) -> Bean:
        """通过ref找到对于的bean"""

        def is_ref_bean(bean: Bean) -> bool:
            if ref.type is RefType.Cls:
                return bean.cls == ref.target
            elif ref.type is RefType.Id:
                return bean.id == ref.target
            else:
                raise ValueError("Unkown RefType {}".format(ref.type))

        valid = list(filter(is_ref_bean, self.id_map.values()))
        if len(valid) == 0:
            raise ValueError("Ref [{}] not existed.".format(ref))
        elif len(valid) > 1:
            raise ValueError("Ref [{}] has multi DepNodes {}".format(ref, valid))
        else:
            return valid[0]

    def get_singleton_cache(self, bean: Bean) -> Optional[Any]:
        """获取singleton缓存"""
        return self.singleton_cache.get(bean.id, None)

    def set_singleton_cache(self, bean: Bean, ins: Any):
        """设置singleton缓存"""
        self.singleton_cache[bean.id] = ins

    def instance(self, ref: Ref, chain_depth: int = 1) -> Any:
        """获取实例对象"""
        bean = self.find_bean_by_ref(ref)

        def debug(msg):
            getattr(self.logger, 'debug')(" " + ">" * chain_depth + ' ' + msg)

        existed_instance_cache = self.get_singleton_cache(bean)
        if bean.singleton and existed_instance_cache:
            debug("retrieved {}".format(bean))
            return existed_instance_cache

        debug("instancing {}".format(bean))

        actual_params: Dict[str, Any] = {}
        for p in bean.params:
            if p.type is PropertyType.Const:
                actual_params[p.name] = p.value
            elif p.type is PropertyType.Ref:
                actual_params[p.name] = self.instance(p.value, chain_depth + 1)
            else:
                raise ValueError("Unkown PropertyType {}".format(p.type))

        ins = get_cls_from_name(bean.cls)(**actual_params)

        self.set_singleton_cache(bean, ins)

        debug("instanced {}".format(bean))

        return ins

    def instance_by_id(self, id: str):
        return self.instance(IdRef(id))

    def instance_by_cls(self, cls: type):
        return self.instance(ClsRef(cls))

    def add_bean(self, cls: Union[str, type], id: str, params: List[Property], singleton: bool):
        if type(cls) is type:
            cls = get_cls_name(cls)

        bean = Bean(cls=cls,
                    id=id,
                    params=params,
                    singleton=singleton)

        self.id_map[id] = bean
        self.cls_map.setdefault(cls, []).append(bean)

    #

    def register(self,
                 cls: type,
                 singleton: bool = True,
                 id: Optional[str] = None,
                 refs: Optional[Dict[str, Ref]] = None,
                 consts: Optional[Dict[str, Any]] = None):
        """程序中注册Bean"""
        id = id or get_cls_name(cls)
        params = self.build_params(cls, refs or {}, consts or {})
        self.add_bean(cls=cls, id=id, params=params, singleton=singleton)

    def register_group(self, group: str = 'default'):
        """注册一批装饰器定义的Beans"""
        for ri in get_collected_group(group):
            self.register(
                cls=ri.cls,
                refs=ri.refs,
                consts=ri.consts,
                singleton=ri.singleton,
                id=ri.id,
            )

    def register_file(self, definition_file: str = './beans.xml'):
        """通过xml文件注册beans"""
        dom = xml.dom.minidom.parse(definition_file)
        bean_list = dom.getElementsByTagName("bean")

        for bean_elem in bean_list:
            cls = bean_elem.getAttribute("cls")
            id = bean_elem.getAttribute("id")
            singleton = json.loads(bean_elem.getAttribute("singleton"))
            prop_elem_list = bean_elem.getElementsByTagName("property")
            param_list: List[Property] = []
            for prop_elem in prop_elem_list:
                name = prop_elem.getAttribute("name")
                ref_expr = prop_elem.getAttribute("ref")
                value_expr = prop_elem.getAttribute("value")
                if ref_expr:
                    type = PropertyType.Ref
                    value = Ref.from_expr(ref_expr)
                elif value_expr:
                    type = PropertyType.Const
                    value_type = prop_elem.getAttribute("value-type") or "str"
                    value = {
                        "str": str,
                        "int": int,
                        "float": float,
                        "bool": lambda v: v.lower()=="true",
                    }[value_type](value_expr)
                else:
                    raise ValueError("property tag need 'ref' or 'value' attributes")

                param_list.append(Property(name=name, type=type, value=value))

            self.add_bean(cls=cls, id=id, singleton=singleton, params=param_list)
