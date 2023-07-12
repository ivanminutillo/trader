# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2023 Valory AG
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

"""This module contains the round behaviour for the 'decision_maker_abci' skill."""

from typing import Set, Type

from packages.valory.skills.abstract_round_abci.behaviours import (
    AbstractRoundBehaviour,
    BaseBehaviour,
)
from packages.valory.skills.decision_maker_abci.behaviours.bet_placement import (
    BetPlacementBehaviour,
)
from packages.valory.skills.decision_maker_abci.behaviours.blacklisting import (
    BlacklistingBehaviour,
)
from packages.valory.skills.decision_maker_abci.behaviours.decision_maker import (
    DecisionMakerBehaviour,
)
from packages.valory.skills.decision_maker_abci.behaviours.sampling import (
    SamplingBehaviour,
)
from packages.valory.skills.decision_maker_abci.rounds import DecisionMakerAbciApp


class AgentDecisionMakerRoundBehaviour(AbstractRoundBehaviour):
    """This behaviour manages the consensus stages for the decision-making."""

    initial_behaviour_cls = DecisionMakerBehaviour
    abci_app_cls = DecisionMakerAbciApp
    behaviours: Set[Type[BaseBehaviour]] = {
        SamplingBehaviour,  # type: ignore
        DecisionMakerBehaviour,  # type: ignore
        BlacklistingBehaviour,  # type: ignore
        BetPlacementBehaviour,  # type: ignore
    }