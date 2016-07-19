# *************************************************************************
# Copyright (c) 2013 Cisco Systems, Inc.  All rights reserved.
# *************************************************************************
from cobra.mit.naming import Dn
from cobra.mit.naming import Rn


class MoStatus(object):
    # Status Constants
    CLEAR = 1
    CREATED = 2
    MODIFIED = 4
    DELETED = 8

    @classmethod
    def fromString(cls, statusStr):
        status = MoStatus(0)
        if statusStr:
            codes = statusStr.split(',')
            for code in codes:
                strippedCode = code.strip()
                if strippedCode == 'created':
                    status.onBit(MoStatus.CREATED)
                elif strippedCode == 'modified':
                    status.onBit(MoStatus.MODIFIED)
                elif strippedCode == 'deleted':
                    status.onBit(MoStatus.DELETED)
        return status

    def __init__(self, status):
        self.__status = status

    @property
    def created(self):
        return (self.__status & MoStatus.CREATED) != 0

    @property
    def deleted(self):
        return (self.__status & MoStatus.DELETED) != 0

    @property
    def modified(self):
        return (self.__status & MoStatus.MODIFIED) != 0

    @property
    def value(self):
        return self.__status

    def update(self, newStatus):
        self.__status = newStatus.value

    def onBit(self, status):
        self.__status |= status

    def offBit(self, status):
        self.__status &= ~status

    def clear(self):
        self.__status = 0

    def __str__(self):
        if self.deleted:
            return 'deleted'
        status = ''
        if self.created:
            status += 'created'
        if self.modified:
            if len(status):
                status += ',modified'
            else:
                status += 'modified'
        return status

    def __cmp__(self, other):
        if other is None:
            return -1
        return self.__status, other.status


class BaseMo(object):
    class _ChildContainer(object):
        class _ClassContainer(object):
            def __init__(self, childClass):
                self._childClass = childClass

                # Key is the tuple of naming props and value is the child Mo
                self._childObjects = {}

            def __getitem__(self, key):
                return self._childObjects[key]

            def __contains__(self, key):
                return key in self._childObjects

            def __setitem__(self, key, value):
                self._checkKey(key, value)
                self._childObjects[key] = value

            def __delitem__(self, key):
                del self._childObjects[key]

            def __len__(self):
                return len(self._childObjects)

            def __iter__(self):
                return iter(self._childObjects.values())

            @property
            def childClass(self):
                return self._childClass

            def _checkKey(self, key, mo):
                meta = self._childClass.meta
                numNamingProps = len(meta.namingProps)
                namingVals = []
                if numNamingProps == 0:
                    if key is not None:
                        raise ValueError('"%s" is bad key for "%s"' %
                                         (str(key), meta.className))
                elif numNamingProps > 1:
                    if not isinstance(key, tuple):
                        raise ValueError('"%s" requires tuple of naming props'
                                         % meta.className)
                    elif len(key) != numNamingProps:
                        raise ValueError('"%s" requires "%d" naming props'
                                         % (meta.className, numNamingProps))
                    namingVals.extend(key)
                else:
                    namingVals.append(key)

                namingValsIter = iter(namingVals)
                for propMeta in meta.namingProps:
                    moVal = getattr(mo, propMeta.name)
                    keyVal = namingValsIter.next()
                    if moVal != keyVal:
                        raise ValueError("'%s' must be '%s' for mo '%s'" %
                                         (keyVal, moVal, str(mo.rn)))

            def clone(self, parentMo, depth):
                newChildContainer = BaseMo._ChildContainer._ClassContainer(self._childClass)
                for nameTuple, childMo in self._childObjects.iteritems():
                    newChildContainer._childObjects[nameTuple] = childMo.clone(parentMo=parentMo, depth=depth)
                return newChildContainer

        class _ChildIter(object):
            def __init__(self, classContainers):
                self._containers = iter(classContainers.values())
                self._currentContainer = None

            def next(self):
                if self._currentContainer is None:
                    # If no more containers this statement will throw an
                    # StopIteration exception and we exit else we move on
                    # to the next container
                    self._currentContainer = iter(self._containers.next())
                try:
                    return self._currentContainer.next()
                except StopIteration:
                    # Current container is done, see if we have anything else
                    self._currentContainer = None
                    return self.next()

            def __iter__(self):
                return self

        def __init__(self, classMeta):
            self._classMeta = classMeta

            # Key is the first rn prefix without the leading '-' if any
            self._classContainers = {}

        def clone(self, parentMo, depth):
            newChildContainer = BaseMo._ChildContainer(self._classMeta)
            for classPrefix, classContainer in self._classContainers.iteritems():
                newChildContainer._classContainers[classPrefix] = classContainer.clone(parentMo, depth)
            return newChildContainer

        def _getChildContainerByMo(self, childMo):
            childMeta = childMo.meta
            childPrefix = childMeta.rnPrefixes[0][0].rstrip('-')
            classContainer = self._classContainers.get(childPrefix, None)
            if classContainer is None:
                if childMeta.className in self._classMeta.childClasses or childMeta.isWireOnly:
                    classContainer = BaseMo._ChildContainer._ClassContainer(childMo.__class__)
                    self._classContainers[childPrefix] = classContainer
                else:
                    raise AttributeError('No class with prefix "{0}" found'.format(childPrefix))
            return classContainer

        def _getChildContainer(self, childPrefix):
            childPrefix = childPrefix.rstrip('-')
            classContainer = self._classContainers.get(childPrefix, None)
            if classContainer is None:
                for childClass in self._classMeta.childClasses:
                    childMeta = childClass.meta
                    prefix = childMeta.rnPrefixes[0][0].rstrip('-')
                    if childPrefix == prefix:
                        classContainer = BaseMo._ChildContainer._ClassContainer(childClass)
                        self._classContainers[childPrefix] = classContainer
                        break
                if classContainer is None:
                    # Could not find a child class with this prefix
                    raise AttributeError('No class with prefix "%s" found' %
                                         childPrefix)
            return classContainer

        def __iter__(self):
            return BaseMo._ChildContainer._ChildIter(self._classContainers)

        def __len__(self):
            numChildren = 0
            for _, classContainer in self._classContainers.iteritems():
                numChildren += len(classContainer)
            return numChildren

    def __init__(self, parentMoOrDn, markDirty, *namingVals,
                 **creationProps):

        if self.__class__ == BaseMo:
            raise NotImplementedError('BaseMo cannot be instantiated.')

        self.__dict__['_BaseMo__meta'] = self.__class__.meta
        if 'status' in creationProps:
            self.__dict__['_BaseMo__status'] = MoStatus.fromString(creationProps['status'])
            del creationProps['status']
        else:
            self.__dict__['_BaseMo__status'] = MoStatus(MoStatus.CREATED | MoStatus.MODIFIED)
        self.__dict__['_BaseMo__dirtyProps'] = set()
        self.__dict__['_BaseMo__children'] = BaseMo._ChildContainer(self.__meta)
        self.__dict__['_BaseMo__rn'] = Rn(self.__meta, *namingVals)
        self.__dict__['_BaseMo__dn'] = None

        if isinstance(parentMoOrDn, str):
            self.__dict__['_BaseMo__parentDnStr'] = parentMoOrDn
            self.__dict__['_BaseMo__parentDn'] = None
            self.__dict__['_BaseMo__parentMo'] = None
        elif isinstance(parentMoOrDn, unicode):
            self.__dict__['_BaseMo__parentDnStr'] = str(parentMoOrDn)
            self.__dict__['_BaseMo__parentDn'] = None
            self.__dict__['_BaseMo__parentMo'] = None
        elif isinstance(parentMoOrDn, Dn):
            self.__dict__['_BaseMo__parentDn'] = parentMoOrDn.clone()
            self.__dict__['_BaseMo__parentMo'] = None
        elif isinstance(parentMoOrDn, BaseMo):
            self.__dict__['_BaseMo__parentMo'] = parentMoOrDn
            self.__dict__['_BaseMo__parentDn'] = parentMoOrDn.dn.clone()
        else:
            raise ValueError('parent mo or dn must be specified')

        # Set the naming props
        self.__dirtyProps.add('status')
        namingValsIter = iter(namingVals)
        for namingPropMeta in self.__meta.namingProps:
            propName = namingPropMeta.name
            value = namingValsIter.next()
            value = namingPropMeta.makeValue(value)
            self.__dict__[propName] = value
            self.__dirtyProps.add(propName)

        # Set the creation props
        props = self.__meta.props
        for name, value in creationProps.items():
            propMeta = props[name]
            value = propMeta.makeValue(value)
            self.__dict__[name] = value
            if markDirty:
                self.__dirtyProps.add(name)

        if self.__parentMo:
            self.__parentMo.__modifyChild(self, attach=True)

    def clone(self, parentMo=None, depth=-1):
        namingVals = self.__rn.namingValueList
        if parentMo is None:
            parentMo = self._parentDn()
        newMo = self.__class__(parentMo, *namingVals, markDirty=False)

        # Copy the properties based on the meta
        for prop in self.__meta.props:
            if prop.isNaming or prop.name == 'rn' or prop.name == 'dn' or prop.name == 'status':
                continue
            name = prop.name
            val = getattr(self, name)
            if name in self.__dirtyProps:
                setattr(newMo, name, val)
            else:
                newMo.__dict__[name] = val

        newMo.status.update(self.__status)

        if depth != 0:
            # Clone the containers to form the subtree recursively
            childDepth = depth - 1
            newMo.__dict__['_BaseMo__children'] = self.__children.clone(parentMo=newMo, depth=childDepth)
        # else we just terminate at the current level

        return newMo

    def update(self, srcMo):
        for dirtyPropName in srcMo.dirtyProps:
            dirtyPropMeta = self.meta.props[dirtyPropName]
            dirtyValue = getattr(srcMo, dirtyPropName)
            if dirtyPropMeta.isCreateOnly:
                self.__dict__[dirtyPropName] = dirtyValue
                self.__dirtyProps.add(dirtyPropName)
            else:
                setattr(self, dirtyPropName, dirtyValue)
        self.__status.update(srcMo.status)

    def isInstance(self, superClassNames):
        moSuperClasses = self.meta.allSuperClassNames()
        superClassNames = set(superClassNames)
        return len(superClassNames & moSuperClasses) > 0

    def __getattr__(self, attrName):
        if attrName in self.meta.props:
            # need to do lazy initialization of this prop to default value
            propMeta = self.meta.props[attrName]
            defValue = propMeta.defaultValueStr
            self.__setprop(propMeta, attrName, defValue, markDirty=False,
                           forced=True)
            return defValue

        # We got this call because properties did not match, so look for
        # child class containers
        return self.__children._getChildContainer(attrName)

    def __setattr__(self, attrName, attrValue):
        if attrName in self.meta.props:
            propMeta = self.meta.props[attrName]
            self.__setprop(propMeta, attrName, attrValue)
        elif attrName.startswith('_BaseMo__'):
            self.__dict__[attrName] = attrValue
        else:
            raise AttributeError('property "%s" not found' % attrName)

    def __setprop(self, propMeta, propName, propValue, markDirty=True,
                  forced=False):
        value = propMeta.makeValue(propValue)
        if propMeta.isDn:
            raise ValueError("dn cannot be set")
        elif propMeta.isRn:
            raise ValueError("rn cannot be set")
        elif propMeta.isCreateOnly and not forced:
            raise ValueError('createOnly "%s" property cannot be set' %
                             propName)

        # Set the attribute to the object dict and mark it dirty
        self.__dict__[propName] = value

        if markDirty:
            self.__setModified()
            self.__dirtyProps.add(propName)

    def __setModified(self):
        self.__status.onBit(MoStatus.MODIFIED)
        self.__dirtyProps.add('status')

    def __modifyChild(self, childMo, attach):
        childMeta = childMo.meta
        namingVals = []
        for nPropMeta in childMeta.namingProps:
            namingVals.append(getattr(childMo, nPropMeta.name))
        childContainer = self.__children._getChildContainerByMo(childMo)
        if len(namingVals) == 0:
            if attach:
                childContainer[None] = childMo
            else:
                del childContainer[None]
        elif len(namingVals) == 1:
            if attach:
                childContainer[namingVals[0]] = childMo
            else:
                del childContainer[namingVals[0]]
        else:
            nvKey = tuple(namingVals)
            if attach:
                childContainer[nvKey] = childMo
            else:
                del childContainer[nvKey]

    def _setParent(self, parentMo):
        self.__parentMo = parentMo
        if parentMo is not None:
            self.__parentDn = parentMo.dn.clone()
        else:
            self.__parentDn = None

    def _attachChild(self, childMo):
        pMo = childMo.parent
        if pMo is not None:
            # Detach from the current parent
            pMo._detachChild(childMo)

        self.__modifyChild(childMo, True)
        childMo._setParent(self)

    def _detachChild(self, childMo):
        if childMo.parent != self:
            raise ValueError('{0} is not attached to {1}'.format(str(self.dn), str(childMo.dn)))
        self.__modifyChild(childMo, False)
        childMo._setParent(None)

    def _delete(self):
        self.__status.clear()
        self.__status.onBit(MoStatus.DELETED)
        self.__dirtyProps.add('status')

    def _dn(self):
        if self.__dn is None:
            self.__dn = self._parentDn().clone()
            self.__dn.appendRn(self.__rn)
        return self.__dn

    def _rn(self):
        return self.__rn

    def _status(self):
        return self.__status

    def _parentDn(self):
        if self.__parentDn is None:
            self.__parentDn = Dn.fromString(self.__parentDnStr)
        return self.__parentDn

    def _parent(self):
        return self.__parentMo

    def _dirtyProps(self):
        return iter(self.__dirtyProps)

    def _children(self):
        return iter(self.__children)

    def _numChildren(self):
        return len(self.__children)

    def _resetProps(self):
        self.__dirtyProps = set()

    def _isPropDirty(self, propName):
        return propName in self.__dirtyProps
