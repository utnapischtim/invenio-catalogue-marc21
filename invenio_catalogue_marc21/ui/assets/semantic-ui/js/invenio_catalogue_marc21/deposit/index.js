/*
 * SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
 * SPDX-License-Identifier: MIT
 */

import React from "react";
import ReactDOM from "react-dom";

import { getInputFromDOM } from "@js/invenio_rdm_records";

import { CatalogueDepositForm } from "./CatalogueDepositForm";

const depositContainerDiv = document.getElementById("marc21-catalogue-deposit-page");

if (depositContainerDiv) {
  ReactDOM.render(
    <CatalogueDepositForm
      record={getInputFromDOM("marc21-catalogue-deposit-record")}
      files={getInputFromDOM("marc21-catalogue-deposit-files")}
      config={getInputFromDOM("marc21-catalogue-deposit-config")}
      templates={getInputFromDOM("marc21-catalogue-deposit-templates")}
      permissions={getInputFromDOM("marc21-catalogue-deposit-permissions")}
    />,
    depositContainerDiv
  );
}
