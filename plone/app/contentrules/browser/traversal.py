# -*- coding: utf-8 -*-
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IRule
from Products.CMFCore.interfaces import ISiteRoot
from zope.component import adapts
from zope.component import getUtility
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.traversing.interfaces import ITraversable


@implementer(ITraversable)
class RuleNamespace(object):
    """Used to traverse to a rule.

    Traversing to portal/++rule++foo will retrieve the rule with id 'foo'
    stored in context, acquisition-wrapped.
    """
    adapts(ISiteRoot, IBrowserRequest)

    def __init__(self, context, request=None):
        self.context = context
        self.request = request

    def traverse(self, name, ignore):
        manager = getUtility(IRuleStorage)
        return manager[name]


@implementer(ITraversable)
class RuleConditionNamespace(object):
    """Used to traverse to a rule condition

    Traversing to portal/++rule++foo/++condition++1 will retrieve the second
    condition of the rule rule with id 'foo', acquisition-wrapped.
    """
    adapts(IRule, IBrowserRequest)

    def __init__(self, context, request=None):
        self.context = context
        self.request = request

    def traverse(self, name, ignore):
        condition = self.context.conditions[int(name)]
        traversal_id = '++condition++{0}'.format(name)
        if condition.id != traversal_id:
            condition.__name__ = condition.id = traversal_id
        return condition


@implementer(ITraversable)
class RuleActionNamespace(object):
    """Used to traverse to a rule condition

    Traversing to portal/++rule++foo/++action++1 will retrieve the second
    condition of the rule rule with id 'foo', acquisition-wrapped.
    """
    adapts(IRule, IBrowserRequest)

    def __init__(self, context, request=None):
        self.context = context
        self.request = request

    def traverse(self, name, ignore):
        action = self.context.actions[int(name)]
        traversal_id = '++action++{0}'.format(name)
        if action.id != traversal_id:
            action.__name__ = action.id = traversal_id
        return action
