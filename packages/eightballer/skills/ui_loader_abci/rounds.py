# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2024 Valory AG
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

"""This package contains the rounds of ComponentLoadingAbciApp."""

from enum import Enum
from typing import Dict, FrozenSet, List, Optional, Set, Tuple

from packages.valory.skills.abstract_round_abci.base import (
    AbciApp,
    AbciAppTransitionFunction,
    AbstractRound,
    AppState,
    BaseSynchronizedData,
    DegenerateRound,
    EventToTimeout,
)

from packages.eightballer.skills.ui_loader_abci.payloads import (
    ErrorPayload,
    HealthcheckPayload,
    SetupPayload,
)


class Event(Enum):
    """ComponentLoadingAbciApp Events"""

    DONE = "done"
    ERROR = "error"


class SynchronizedData(BaseSynchronizedData):
    """
    Class to represent the synchronized data.

    This data is replicated by the tendermint application.
    """


class ErrorRound(AbstractRound):
    """ErrorRound"""

    payload_class = ErrorPayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    # TODO: replace AbstractRound with one of CollectDifferentUntilAllRound,
    # CollectSameUntilAllRound, CollectSameUntilThresholdRound,
    # CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound,
    # from packages/valory/skills/abstract_round_abci/base.py
    # or implement the methods

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError

    def check_payload(self, payload: ErrorPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: ErrorPayload) -> None:
        """Process payload."""
        raise NotImplementedError


class HealthcheckRound(AbstractRound):
    """HealthcheckRound"""

    payload_class = HealthcheckPayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    # TODO: replace AbstractRound with one of CollectDifferentUntilAllRound,
    # CollectSameUntilAllRound, CollectSameUntilThresholdRound,
    # CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound,
    # from packages/valory/skills/abstract_round_abci/base.py
    # or implement the methods

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError

    def check_payload(self, payload: HealthcheckPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: HealthcheckPayload) -> None:
        """Process payload."""
        raise NotImplementedError


class SetupRound(AbstractRound):
    """SetupRound"""

    payload_class = SetupPayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    # TODO: replace AbstractRound with one of CollectDifferentUntilAllRound,
    # CollectSameUntilAllRound, CollectSameUntilThresholdRound,
    # CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound,
    # from packages/valory/skills/abstract_round_abci/base.py
    # or implement the methods

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError

    def check_payload(self, payload: SetupPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: SetupPayload) -> None:
        """Process payload."""
        raise NotImplementedError


class DoneRound(DegenerateRound):
    """DoneRound"""


class ComponentLoadingAbciApp(AbciApp[Event]):
    """ComponentLoadingAbciApp"""

    initial_round_cls: AppState = SetupRound
    initial_states: Set[AppState] = {HealthcheckRound, SetupRound}
    transition_function: AbciAppTransitionFunction = {
        SetupRound: {
            Event.DONE: HealthcheckRound,
            Event.ERROR: ErrorRound
        },
        HealthcheckRound: {
            Event.DONE: DoneRound,
            Event.ERROR: ErrorRound
        },
        ErrorRound: {
            Event.DONE: SetupRound
        },
        DoneRound: {}
    }
    final_states: Set[AppState] = {DoneRound}
    event_to_timeout: EventToTimeout = {}
    cross_period_persisted_keys: FrozenSet[str] = frozenset()
    db_pre_conditions: Dict[AppState, Set[str]] = {
        HealthcheckRound: set([]),
    	SetupRound: set([]),
    }
    db_post_conditions: Dict[AppState, Set[str]] = {
        DoneRound: set([]),
    }
