/*
 * SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
 * SPDX-License-Identifier: MIT
 */

import PropTypes from "prop-types";
import React from "react";
import { Card } from "semantic-ui-react";

import { Tree } from "./Tree";

export const CatalogueTree = ({ catalogue }) => {
  return (
    <Card className="catalogue-field" fluid>
      <Card.Content>
        <Tree data={catalogue} />
      </Card.Content>
    </Card>
  );
};

CatalogueTree.propTypes = {
  catalogue: PropTypes.object.isRequired,
};
