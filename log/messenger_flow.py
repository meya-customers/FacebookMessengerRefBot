from dataclasses import dataclass
from meya.entry import Entry
from meya.http.direction import Direction
from meya.http.entry.request import HttpRequestEntry
from meya.lifecycle.event.event import LifecycleEvent
from meya.log.element import LogElement
from typing import List

INTEGRATION_ID = "integration.facebook.messenger"


@dataclass
class MessengerFlowElement(LogElement):
    async def process(self) -> List[Entry]:
        entries = []
        if (
            isinstance(self.entry, HttpRequestEntry)
            and self.entry.url.startswith(
                "http://grid.meya.ai/gateway/v2/facebook_messenger/app-"
            )
            and self.entry.direction == Direction.RX
        ):
            try:
                ref = self.entry.data["entry"][0]["messaging"][0]["postback"][
                    "referral"
                ]["ref"]
            except KeyError:
                ref = None
            if ref:
                # identify thread and user
                message = self.entry.data["entry"][0]["messaging"][0]
                sender_id = message["sender"]["id"]
                page_id = int(message["recipient"]["id"])
                await self.user.identify(
                    sender_id,
                    integration_id=INTEGRATION_ID,
                    data=dict(page_id=page_id, sender_id=sender_id),
                )
                await self.thread.identify(
                    sender_id,
                    integration_id=INTEGRATION_ID,
                    data=dict(
                        primary_user_id=self.user.id,
                        page_id=page_id,
                        sender_id=sender_id,
                    ),
                )
                # emit a lifecycle event
                entries.append(
                    LifecycleEvent(
                        user_id=self.user.id,
                        thread_id=self.thread.id,
                        integration_id=INTEGRATION_ID,
                        context={},
                        lifecycle_id="get_started",
                        text=ref,
                    )
                )
        return entries
