/*
 * SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
 * SPDX-License-Identifier: MIT
 */

import PropTypes from "prop-types";

export const CatalogueTreeItem = ({ nodeData = {}, nodeToggle }) => {
  return (
    <g>
      <text style={{ font: "italic 20px serif", fill: "black" }} onClick={nodeToggle}>
        {nodeData.name}
      </text>
    </g>
  );
};

export const renderCustomNode = ({ nodeDatum, toggleNode }) => (
  <CatalogueTreeItem nodeData={nodeDatum} triggerNodeToggle={toggleNode} />
);

CatalogueTreeItem.propTypes = {
  nodeData: PropTypes.object.isRequired,
  nodeToggle: PropTypes.func.isRequired,
};
