/*
 * SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
 * SPDX-License-Identifier: MIT
 */

import PropTypes from "prop-types";
import React, { Component } from "react";
import { Card, Divider, Grid } from "semantic-ui-react";

import { DeleteButton, SaveButton } from "@js/invenio_rdm_records";
import { PublishButton } from "@js/invenio_rdm_records/src/deposit/controls/PublishButton/PublishButton";
import {
  FilesAccess,
  MetadataAccess,
} from "@js/invenio_rdm_records/src/deposit/fields/AccessField/components";
import { TemplateField } from "@js/invenio_records_marc21/components";
import { i18next } from "@translations/invenio_catalogue_marc21/i18next";

import { Expandable } from "./../../utils/expandable";
import { UploadCSV } from "./UploadCSV";
import { UploadFiles } from "./UploadFiles";

export class ManageRecord extends Component {
  constructor(props) {
    super(props);
  }

  state = {};

  render() {
    const { record, permissions, templates, config } = this.props;

    return (
      <Card>
        <Card.Content>
          <Grid relaxed>
            <Grid.Column width={16}>
              <SaveButton fluid />
              <PublishButton fluid doiReservationCheck={() => false} />

              {permissions.can_delete_draft && (
                <DeleteButton
                  fluid
                  // TODO: make is_published part of the API response
                  //       so we don't have to do this
                  isPublished={record.is_published}
                />
              )}

              {templates.length > 0 && (
                <TemplateField
                  label={i18next.t("Templates")}
                  labelIcon="bookmark"
                  templates={templates}
                />
              )}

              {permissions.showMetadataAccess && (
                <>
                  <MetadataAccess record={record} />
                  <Divider hidden />
                </>
              )}

              {permissions.showFileAccess && (
                <>
                  <FilesAccess />
                  <Divider hidden />
                </>
              )}

              {permissions.showFileUploader && (
                <UploadFiles record={record} config={config} />
              )}

              {permissions.showUploadCSV && (
                <UploadCSV record={record} config={config} />
              )}

              <Expandable
                id="InvenioCatalogueMarc21.Manage.Container"
                record={record}
                config={config}
              />
            </Grid.Column>
          </Grid>
        </Card.Content>
      </Card>
    );
  }
}

ManageRecord.propTypes = {
  record: PropTypes.object.isRequired,
  permissions: PropTypes.object.isRequired,
  templates: PropTypes.object.isRequired,
  config: PropTypes.object.isRequired,
};
