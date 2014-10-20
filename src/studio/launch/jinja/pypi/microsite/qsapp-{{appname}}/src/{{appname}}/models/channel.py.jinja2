# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import url_for
from studio.core.engines import db
from microsite.models.article import ArticleModel


def articles_order_by():
    return [db.desc(ArticleModel.is_sticky),
            db.desc(ArticleModel.date_published)]


class ChannelModel(db.Model):
    __tablename__ = 'channel'

    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    name = db.Column(db.Unicode(64), nullable=False, unique=True, index=True)
    introduction = db.Column(db.Unicode(1024), nullable=True)

    articles = db.relationship(
        'ArticleModel',
        primaryjoin='and_(ChannelModel.id==ArticleModel.cid,'
                    'ArticleModel.date_published<=func.now())',
        order_by=articles_order_by,
        foreign_keys='[ArticleModel.cid]',
        passive_deletes='all', lazy='dynamic')

    all_articles = db.relationship(
        'ArticleModel',
        primaryjoin='ChannelModel.id==ArticleModel.cid',
        order_by=articles_order_by,
        foreign_keys='[ArticleModel.cid]',
        backref=db.backref(
            'channel', lazy='joined', innerjoin=True),
        passive_deletes='all', lazy='dynamic')

    @property
    def url(self):
        return url_for("views.channel", cid=self.id)

    def __str__(self):
        return self.name
