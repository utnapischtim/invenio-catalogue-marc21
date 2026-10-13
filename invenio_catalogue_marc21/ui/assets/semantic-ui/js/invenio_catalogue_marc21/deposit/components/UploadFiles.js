/*
 * SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
 * SPDX-License-Identifier: MIT
 */

import PropTypes from "prop-types";
import React, { PureComponent } from "react";
import { connect } from "react-redux";
import {
  Button,
  Modal,
  ModalActions,
  ModalContent,
  ModalHeader,
} from "semantic-ui-react";

import { FileUploader } from "@js/invenio_rdm_records";

function modalLocalReducer(state, action) {
  switch (action.type) {
    case "close":
      return { ...state, open: false };
    case "open":
      return { ...state, open: true, size: action.size };
    case "upload":
      return { ...state, open: false };
    default:
      return state;
  }
}

class UploadFilesCmp extends PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      open: false,
      size: undefined,
    };
    this.inputRef = React.createRef();
  }

  dispatch = (action) => {
    this.setState((prevState) => modalLocalReducer(prevState, action));
  };

  handleOpen = () => {
    this.dispatch({ type: "open", size: "large" });
  };

  handleClose = () => {
    this.dispatch({ type: "close" });
  };

  render() {
    const { open, size } = this.state;
    const { record, config } = this.props;

    record["access"] = { record: "public", files: "public" };
    record["files"]["enabled"] = true;

    return (
      <>
        <Button
          compact
          fluid
          onClick={this.handleOpen}
          icon="file"
          labelPosition="left"
          content="Upload Files"
        />
        <Modal size={size} open={open} onClose={this.handleClose}>
          <ModalHeader>Upload Files + zip file</ModalHeader>
          <ModalContent>
            <FileUploader
              isDraftRecord={!record.is_published}
              quota={config.quota}
              record={record}
            />
          </ModalContent>
          <ModalActions>
            <Button negative onClick={this.handleClose}>
              Close
            </Button>
          </ModalActions>
        </Modal>
      </>
    );
  }
}

UploadFilesCmp.propTypes = {
  record: PropTypes.object.isRequired,
  config: PropTypes.object.isRequired,
};

const mapStateToProps = null;

const mapDispatchToProps = null;

export const UploadFiles = connect(mapStateToProps, mapDispatchToProps)(UploadFilesCmp);
