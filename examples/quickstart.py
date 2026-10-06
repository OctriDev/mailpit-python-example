"""Capture a message in local Mailpit and verify its typed responses."""

import asyncio
import os

from octri_mailpit_example import ClientConfig, Mailpit, create_send_message_params_attachments_item
from octri_mailpit_example.types import SendMessageParamsFrom, SendMessageParamsToItem


async def main() -> None:
    sdk = Mailpit(ClientConfig(base_url=os.getenv("MAILPIT_BASE_URL", "http://localhost:8025")))
    subject = "octri-python-example"
    text = "A typed SDK example, captured locally by Mailpit."
    sent = await sdk.message.send_params(
        from_=SendMessageParamsFrom(Email="sender@example.test", Name="Octri example"),
        to=[SendMessageParamsToItem(Email="recipient@example.test", Name="Example recipient")],
        subject=subject,
        text=text,
        html=f"<p>{text}</p>",
        attachments=[
            create_send_message_params_attachments_item(
                {
                    "Content": "AP9/gA==",
                    "Filename": "example.bin",
                    "ContentType": "application/octet-stream",
                }
            )
        ],
    )
    assert isinstance(sent.id, str) and sent.id, "Mailpit must return the new message ID"

    inbox = await sdk.messages.get_params(limit=10)
    assert isinstance(inbox.messages, list)
    assert any(message.id == sent.id for message in inbox.messages)
    results = await sdk.messages.search_params(query=f"subject:{subject}")
    assert isinstance(results.messages, list)
    message = next(item for item in results.messages if item.id == sent.id)
    assert message.subject == subject
    assert message.bcc is None
    assert message.cc is None
    assert message.reply_to is None

    body = await sdk.testing.get_message_text_params(id=sent.id)
    assert body.strip() == text
    html = await sdk.testing.get_message_html_params(id=sent.id)
    assert text in html
    detail = await sdk.message.get_params(id=sent.id)
    assert isinstance(detail.attachments, list) and detail.attachments
    part_id = detail.attachments[0].part_id
    assert isinstance(part_id, str) and part_id
    attachment = await sdk.message.attachment_params(id=sent.id, part_id=part_id)
    assert attachment == bytes([0, 255, 127, 128])
    print(f"Captured {sent.id}; verified send, list, search, text, HTML, and binary retrieval.")


if __name__ == "__main__":
    asyncio.run(main())
