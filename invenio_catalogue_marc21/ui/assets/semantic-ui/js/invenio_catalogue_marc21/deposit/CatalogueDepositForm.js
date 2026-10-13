/*
 * SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
 * SPDX-License-Identifier: MIT
 */

import React, { Component } from "react";
import { Grid } from "semantic-ui-react";

import { DepositFormApp, FormFeedback } from "@js/invenio_rdm_records";
import { MetadataFields } from "@js/invenio_records_marc21/components";
import { i18next } from "@translations/invenio_catalogue_marc21/i18next";

import { ExpandableContext, expandableStore } from "./../utils/expandable";
import { CatalogueTree, ManageRecord, Marc21CatalogueSerializer } from "./components";

export class CatalogueDepositForm extends Component {
  constructor(props) {
    super(props);

    const { files, record } = this.props;

    this.props = props;
    this.config = props.config || {};
    this.templates = props.templates || [];
    this.files = props.files;
    this.recordSerializer = new Marc21CatalogueSerializer();

    this.noFiles = false;
    if (
      !Array.isArray(files.entries) ||
      (!files.entries.length && record.is_published)
    ) {
      this.noFiles = true;
    }
  }

  accordionStyle = {
    header: { className: "segment inverted brand" },
  };

  render() {
    const { record, files, permissions, preselectedCommunity } = this.props;
    const allowRecordRestriction = true;
    const expandableComponents = expandableStore.getAll();
    const sectionsConfig = {};

    return (
      <ExpandableContext.Provider value={expandableComponents}>
        <DepositFormApp
          config={this.config}
          record={record}
          preselectedCommunity={preselectedCommunity}
          files={files}
          permissions={permissions}
          recordSerializer={this.recordSerializer}
        >
          <FormFeedback fieldPath="message" sectionsConfig={sectionsConfig} />
          <>
            {this.noFiles && record.is_published && (
              <div className="text-align-center pb-10">
                <em>{i18next.t("The record has no files.")}</em>
              </div>
            )}
            <Grid>
              <Grid.Row>
                <Grid.Column className="left-sidebar" computer={5}>
                  <CatalogueTree
                    label={i18next.t("Catalogue")}
                    labelIcon="space shuttle"
                    fieldPath="catalgoue"
                    catalogue={record.tree}
                    onError={() => {}}
                  />
                </Grid.Column>

                <Grid.Column className="main-column" computer={8}>
                  <MetadataFields className="metadata" fieldPath="metadata" />
                </Grid.Column>

                <Grid.Column className="right-sidebar" computer={3}>
                  <ManageRecord
                    record={record}
                    permissions={permissions}
                    alloweRecordRestriction={allowRecordRestriction}
                    templates={this.templates}
                    config={this.config}
                  />
                </Grid.Column>
              </Grid.Row>
            </Grid>
          </>
        </DepositFormApp>
      </ExpandableContext.Provider>
    );
  }
}
