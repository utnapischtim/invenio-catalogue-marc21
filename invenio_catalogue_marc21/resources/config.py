# -*- coding: utf-8 -*-
#
# Copyright (C) 2024-2025 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Catalogue service component for ."""

from flask_resources import RequestBodyParser, ResponseHandler
from flask_resources.parsers import MultiDictSchema
from flask_resources.serializers import JSONSerializer
from invenio_drafts_resources.resources import RecordResourceConfig
from invenio_records_resources.resources.records.args import SearchRequestArgsSchema
from marshmallow.fields import Bool, Int, Str

from .deserializers.deserializer import Marc21CatalogueDeserializer
from .serializers.deposit import Marc21CatalogueDepositSerializer

url_prefix = "/catalogue"


class CatalogueSearchArgsSchema(MultiDictSchema):
    """Search URL query string arguments."""

    drafts = Bool()


class TasksSearchRequestArgsSchema(SearchRequestArgsSchema):
    """Request URL query string arguments."""

    params = Str()


class Marc21CatalogueAlmaProxyResourceConfig(RecordResourceConfig):
    """Marc21 catalogue proxy resource config."""

    blueprint_name: str = "marc21_catalogue_alma_proxy"
    url_prefix: str = url_prefix

    default_accept_mimetype: str = "application/json"

    response_handlers: dict = {
        "application/json": ResponseHandler(Marc21CatalogueDepositSerializer()),
    }

    links_config: dict = {}

    routes: dict = {
        "alma": "/alma/<type>/<pid_value>",
    }

    # Request parsing
    request_search_args = CatalogueSearchArgsSchema  # type: ignore[assignment]
    request_args = SearchRequestArgsSchema
    request_view_args: dict = {
        "pid_value": Str(),
        "type": Str(),
    }
    request_headers: dict = {"if_match": Int()}


class Marc21CatalogueTasksConfig(RecordResourceConfig):
    """Marc21 catalogue progress resource configuration."""

    blueprint_name: str = "marc21_catalogue_tasks"
    url_prefix: str = f"{url_prefix}/tasks"

    routes: dict = {
        "progress": "/progress/<pid_value>",
        "start": "/start/<pid_value>/<task>",  # params is a list
    }

    request_view_args: dict = {
        "pid_value": Str(),
        "task": Str(),
    }
    request_search_args = TasksSearchRequestArgsSchema


class Marc21CatalogueResourceConfig(RecordResourceConfig):
    """Marc21 Record resource configuration."""

    blueprint_name: str = "marc21_catalogue"
    url_prefix: str = url_prefix

    default_accept_mimetype: str = "application/json"

    response_handlers: dict = {
        "application/json": ResponseHandler(Marc21CatalogueDepositSerializer()),
    }

    links_config: dict = {}

    routes: dict = {
        "item": "/<pid_value>/catalogue",
        "add": "/<pid_value>/add",
        "edit": "/<pid_value>/edit",
    }

    # Request parsing
    request_search_args = CatalogueSearchArgsSchema  # type: ignore[assignment]
    request_args = SearchRequestArgsSchema
    request_view_args: dict = {
        "pid_value": Str(),
    }
    request_headers: dict = {"if_match": Int()}
    request_body_parsers: dict = {
        "application/json": RequestBodyParser(Marc21CatalogueDeserializer()),
    }


class Marc21CatalogueRecordResourceConfig(RecordResourceConfig):
    """Marc21 Record resource configuration."""

    blueprint_name: str = "marc21_catalogue_records"
    url_prefix: str = url_prefix

    default_accept_mimetype: str = "application/json"

    response_handlers: dict = {
        "application/json": ResponseHandler(JSONSerializer()),
        "application/vnd.inveniomarc21.v1+json": ResponseHandler(
            Marc21CatalogueDepositSerializer(),
        ),
    }
    links_config: dict = {}

    routes: dict = {
        "search": "/search",
        "list": "",
        "item": "/<pid_value>",
        "item-draft": "/<pid_value>/draft",
        "item-publish": "/<pid_value>/draft/actions/publish",
    }

    # Request parsing
    request_args = SearchRequestArgsSchema
    request_headers: dict = {"if_match": Int()}
    request_body_parsers: dict = {
        "application/json": RequestBodyParser(Marc21CatalogueDeserializer()),
    }

    request_view_args: dict = {
        "pid_value": Str(),
        "pid_type": Str(),
    }
