/*
 * SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
 * SPDX-License-Identifier: MIT
 */

import PropTypes from "prop-types";
import React, { Component } from "react";
import { Header, Icon, List, Message } from "semantic-ui-react";

export class ShowProgress extends Component {
  constructor(props) {
    super(props);
    // item will have the structure:
    // {
    //   title: "..",
    //   messageType: "success" || "error" || "info",
    //   status: "ongoing" || "finished"
    // }
    this.state = {
      items: [], //  messageType: "success" || "error" || "info"
      isPolling: true,
    };

    this.pollInterval = 3000; // miliseconds
  }

  componentDidMount() {
    this.startPolling();
  }

  componentWillUnmount() {
    this.stopPolling();
  }

  startPolling = () => {
    // Set up interval for subsequent requests
    this.pollInterval = setInterval(() => {
      this.checkForUpdates();
    }, this.pollingInterval);
  };

  stopPolling = () => {
    if (this.pollInterval) {
      clearInterval(this.pollInterval);
      this.pollInterval = null;
    }
  };

  checkForUpdates = async () => {
    const { isPolling } = this.state;
    const { recid } = this.props;

    if (!isPolling) {
      return;
    }

    try {
      const response = await fetch(`/api/catalogue/tasks/progress/${recid}`);
      const data = await response.json();
      // the api returns everytime the whole list, not only the newest
      // this simplifies the backend
      this.setState({ items: data });

      if (data.status == "finished") {
        // Stop polling and show completion status
        this.setState({ isPolling: false });
        this.stopPolling();
        return;
      }
    } catch (error) {
      // Handle network or parsing errors
      // maybe this should be done outside of the list?
      this.setState((prevState) => ({
        items: [...prevState.items, { title: error, messageType: "error" }],
      }));
      this.setState({ isPolling: false });
      this.stopPolling();
    }
  };

  render() {
    const { items, isPolling } = this.state;
    const { pollingInterval } = this.props;

    return (
      <div>
        <Header as="h2">
          Progress Monitor
          {isPolling && (
            <Header.Subheader>
              <Icon name="refresh" loading />
              Polling every {pollingInterval} seconds
            </Header.Subheader>
          )}
        </Header>

        {items.length > 0 && (
          <List divided relaxed>
            {items.map((item) => (
              <List.Item key={item.id}>
                <List.Icon name="file text" />
                <List.Content>
                  <List.Header>{item.title}</List.Header>
                </List.Content>
              </List.Item>
            ))}
          </List>
        )}

        {items.length === 0 && (
          <Message>
            <Message.Header>No items yet</Message.Header>
            <p>Waiting for updates from the server...</p>
          </Message>
        )}
      </div>
    );
  }
}

ShowProgress.propTypes = {
  recid: PropTypes.string.isRequired,
  pollingInterval: PropTypes.number.isRequired,
};
