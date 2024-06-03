# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2024 eightballer
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This package contains a scaffold of a behaviour."""
from aea.configurations.base import PublicId
import os
from glob import glob
from pathlib import Path

from aea.cli.utils.config import get_ipfs_node_multiaddr
from aea.skills.base import Model
from aea_cli_ipfs.ipfs_utils import DownloadError, IPFSTool

DEFAULT_FRONTEND_DIR = "./www"
DEFAULT_LOG_FILE = "log.txt"


class UiLoaderStrategy(Model):
    """This class scaffolds a model."""

    clients = {}
    routes: dict = {}

    def __init__(self, **kwargs):
        """Initialize the model."""
        frontend_component = kwargs.pop("frontend_component_id", None)
        if frontend_component is None:
            raise ValueError("frontend_component_id not provided! Please provide a frontend_component_id.")
        super().__init__(**kwargs)
        self.frontend_component_id = PublicId.from_str(frontend_component)


    def setup(self) -> None:
        """
        Configure the frontend.
        """
        self.context.logger.info(f"Setting up frontend for component {self.frontend_component_id}.")
        self.setup_frontend()
        self.context.logger.info("Frontend setup complete.")

    def setup_frontend(self) -> None:
        """
        We pull the frontend from IPFS.
        """
        ipfs_tool = IPFSTool(get_ipfs_node_multiaddr())
        try:
            ipfs_tool.download(self.frontend_component_id.hash, DEFAULT_FRONTEND_DIR)
        except DownloadError as e:
            self.context.logger.error(str(e))
            self.context.logger.error("Failed to download frontend from IPFS.")
            return

        # we generate a mapping of routes based on all the files found in the frontend directory
        self.context.logger.info("Generating routes...")
        self.routes = self.generate_routes()
        self.context.logger.info("Routes generated.")

    def generate_routes(self) -> dict:
        """
        We generate a mapping of routes based on all the files found in the frontend directory.
        We read the files into memory and store them in the routes dict.
        """
        routes = {}
        for path in glob(f"{self.frontend_directory}/**/*", recursive=True):
            data = Path(path)
            if data.is_file():
                route = data.relative_to(self.frontend_directory / "build")
                routes[str(route)] = data.read_bytes()
        return routes
