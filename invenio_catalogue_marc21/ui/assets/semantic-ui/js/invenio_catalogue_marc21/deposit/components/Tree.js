/*
 * SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
 * SPDX-License-Identifier: MIT
 */

import axios from "axios";
import { hierarchy, tree } from "d3-hierarchy";
import { linkHorizontal } from "d3-shape";
import PropTypes from "prop-types";
import React, { Component, createRef } from "react";
import { connect } from "react-redux";

import { ContextMenu } from "./ContextMenu";

class TreeCmp extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: props.data || {},
      tree: undefined,
      contextMenu: { visible: false, x: 0, y: 0, node: null },
    };
    this.svgRef = createRef();
  }

  componentDidMount() {
    this.update();
  }

  componentDidUpdate(prevProps, prevState) {
    const { data } = this.state;
    if (prevState.data !== data) {
      this.update();
    }
  }

  addNode = async (parent, data) => {
    try {
      let apiConfig = {
        withCredentials: true,
        xsrfCookieName: "csrftoken",
        xsrfHeaderName: "X-CSRFToken",
        headers: { Accept: "application/json" },
      };
      let axiosWithConfig = axios.create(apiConfig);
      const url = `/api/catalogue/${parent.data.node}/add`;
      const response = await axiosWithConfig.post(url, data);
      return response.data;
    } catch (error) {
      console.log("CreateNode error: ", error);
      return {};
    }
  };

  editNode = async (node) => {
    try {
      let apiConfig = {
        withCredentials: true,
        xsrfCookieName: "csrftoken",
        xsrfHeaderName: "X-CSRFToken",
        headers: { Accept: "application/json" },
      };
      let axiosWithConfig = axios.create(apiConfig);
      const url = `/api/catalogue/${node.data.node}/edit`;
      const response = await axiosWithConfig.get(url);
      return response.data;
    } catch (error) {
      console.log("CreateNode error: ", error);
      return {};
    }
  };

  update = () => {
    const width = 800;
    const height = 500;
    const { data } = this.state;
    const root = hierarchy(data);
    tree().size([height - 100, width - 200])(root);

    const descendants = root.descendants();
    descendants.forEach((n, i) => (n.x = i * 30));
    descendants.forEach((n) => (n.y = n.depth * 50));

    this.setState({ tree: root });
  };

  handleContextMenu = (event, node) => {
    event.preventDefault();
    this.setState({
      contextMenu: {
        visible: true,
        x: event.clientY - 580,
        y: event.clientX + 8,
        node: node,
      },
    });
  };

  handleMenuClick = (action, node) => {
    switch (action) {
      case "rename":
        break;
      case "add":
        this.add(node);
        break;
      case "edit":
        this.edit(node);
        break;
    }

    const state = {
      contextMenu: {
        visible: false,
        x: 0,
        y: 0,
        node: null,
      },
    };

    this.setState(state);
  };

  handleNodeClick = (event, node) => {
    document.location.href = node.data.self_html;
  };

  add = async (parent) => {
    const parentId = parent.data.node;
    const rootId = parent.data.root == "" ? parent.data.node : parent.data.root;
    const data = { catalogue: { parent: parentId, root: rootId, children: [] } };
    const newChild = await this.addNode(parent, data);

    const { saveAction } = this.props;

    saveAction(newChild);

    if (!parent.data.children) {
      parent.data.children = [];
    }
    parent.data.children.push(newChild);

    this.setState({ data: { ...this.state.data } });
  };

  edit = async (node) => {
    const { saveAction } = this.props;
    const child = await this.editNode(node);
    saveAction(child);
  };

  render() {
    const { tree, contextMenu } = this.state;

    return (
      <>
        <svg
          width="800"
          height={tree && tree.descendants().length * 30 + 100}
          ref={this.svgRef}
          onClick={() => this.setState({ contextMenu: { visible: false } })}
        >
          <g transform="translate(50,50)">
            {tree &&
              tree.links().map((link, i) => (
                <path
                  key={i}
                  d={linkHorizontal()
                    .x((d) => d.y)
                    .y((d) => d.x)(link)}
                  fill="none"
                  stroke="#999"
                />
              ))}
            {tree &&
              tree.descendants().map((node, i) => (
                <g
                  key={i}
                  transform={`translate(${node.y},${node.x})`}
                  onClick={(e) => this.handleNodeClick(e, node)}
                  onContextMenu={(e) => this.handleContextMenu(e, node)}
                >
                  <circle r="8" fill="steelblue" stroke="white" strokeWidth="2" />
                  <text
                    dy="3"
                    x={node.children ? 90 : 10}
                    textAnchor={node.children ? "end" : "start"}
                  >
                    {node.data.name[0].substring(0, 50)}
                    {node.data.name[0].length > 50 && "..."}
                  </text>
                </g>
              ))}
          </g>
        </svg>

        <ContextMenu {...contextMenu} onAction={this.handleMenuClick} />
      </>
    );
  }
}

TreeCmp.propTypes = {
  data: PropTypes.object.isRequired,
  saveAction: PropTypes.func.isRequired,
};

function save(data) {
  // maybe not necessary that complicated but it does work like that
  // name should be different, because it does not save the record
  // it does only updating the record
  return async (dispatch) => {
    dispatch({
      type: "DRAFT_SAVE_SUCCEEDED",
      payload: { data: data },
    });
  };
}

const mapStateToProps = null;

const mapDispatchToProps = (dispatch) => ({
  saveAction: (values) => dispatch(save(values)),
});

export const Tree = connect(mapStateToProps, mapDispatchToProps)(TreeCmp);
