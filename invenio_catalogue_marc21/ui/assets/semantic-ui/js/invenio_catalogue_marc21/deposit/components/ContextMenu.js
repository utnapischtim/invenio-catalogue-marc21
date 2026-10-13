/*
 * SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
 * SPDX-License-Identifier: MIT
 */

import PropTypes from "prop-types";
import React, { PureComponent } from "react";
import { Menu, Popup } from "semantic-ui-react";

export class ContextMenu extends PureComponent {
  render() {
    const { visible, x, y, onAction, node } = this.props;

    if (!visible) {
      return null;
    }

    return (
      <Popup
        open
        position="top left"
        style={{
          position: "absolute",
          top: `${x}px`,
          left: `${y}px`,
          zIndex: 1000,
        }}
      >
        <Menu vertical>
          <Menu.Item
            style={{ cursor: "pointer" }}
            onClick={() => onAction("add", node)}
          >
            Add
          </Menu.Item>
          <Menu.Item
            style={{ cursor: "pointer" }}
            onClick={() => onAction("remove", node)}
          >
            Remove
          </Menu.Item>
          <Menu.Item
            style={{ cursor: "pointer" }}
            onClick={() => onAction("edit", node)}
          >
            Edit
          </Menu.Item>
        </Menu>
      </Popup>
    );
  }
}

ContextMenu.propTypes = {
  visible: PropTypes.bool.isRequired,
  x: PropTypes.number.isRequired,
  y: PropTypes.number.isRequired,
  onAction: PropTypes.func.isRequired,
  node: PropTypes.object.isRequired,
};
