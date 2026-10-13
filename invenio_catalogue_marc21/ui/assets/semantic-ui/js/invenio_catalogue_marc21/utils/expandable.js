/*
 * SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
 * SPDX-License-Identifier: MIT
 */

import PropTypes from "prop-types";
import React, { useContext } from "react";

// create a new context with an empty map of expanded components as default value.
export const ExpandableContext = React.createContext({});

/**
 * React component to enable expanding element when rendering.
 */
function Expandable({ id, children, ...restProps }) {
  const components = useContext(ExpandableContext);
  const child = children ? React.Children.only(children) : null;
  const childProps = child ? child.props : {};

  if (id in components) {
    const elements = components[id].map((ele, i) =>
      React.createElement(ele, { ...childProps, ...restProps, key: `${id}-${i}` })
    );
    return elements;
  } else {
    return null;
  }
}

Expandable.propTypes = {
  /** The children of the component */
  children: PropTypes.node,
  /** The id that the component will be bound to (normally component's name) */
  id: PropTypes.string,
};

Expandable.defaultProps = {
  id: null,
  children: null,
};

/**
 * High-order component to expand an existing React component and provide a new component instead.
 */
Expandable.component = (id, Component) => {
  const Expanded = ({ children, ...props }) => {
    const components = useContext(ExpandableContext);
    return React.createElement(components[id] || Component, props, children);
  };
  Expanded.propTypes = {
    children: PropTypes.oneOfType([PropTypes.node, PropTypes.func]),
  };
  Expanded.defaultProps = {
    children: null,
  };
  const name = Component.displayName || Component.name;
  Expanded.displayName = `Expandable(${name})`;
  Expanded.originalComponent = Component;
  return Expanded;
};

export { Expandable };

/**
 * Simple utility class responsible of keeping track of all expanded components.
 * @constructor object containing the initial map `id: Component` of expanded components
 */
export class ExpandedComponentRepository {
  constructor() {
    this.components = {};
  }

  append = (id, component) => {
    if (!Array.isArray(this.components[id])) {
      this.components[id] = [];
    }
    this.components[id].push(component);
  };

  get = (id) => {
    return this.components[id];
  };

  getAll = () => {
    return { ...this.components };
  };

  clear = () => {
    this.components = {};
  };
}

export const expandableStore = new ExpandedComponentRepository();
