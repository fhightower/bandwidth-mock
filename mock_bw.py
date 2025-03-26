import json
import logging

from mitmproxy import http

from bandwidth_mock.api import mock_messages_response, mock_tndetails


URL_TO_MOCK_MAPPING = {
    "api/messages": mock_messages_response,
    "tndetails": mock_tndetails,
}


def _is_bandwidth_api_request(host: str) -> bool:
    return "bandwidth.com" in host and "api" in host


def request(flow: http.HTTPFlow) -> None:
    server_address = flow.server_conn.address
    client_address = flow.client_conn.address

    logging.info(f"== New request ==")
    logging.info(f"Client: {client_address}")
    logging.info(f"Server: {server_address}")
    logging.info(f"Host (flow.request.host): {flow.request.host}")
    logging.info(f"URL: {flow.request.pretty_url}")
    logging.info("---")

    logging.info(f'Handling request to {flow.request.pretty_url}')
    if _is_bandwidth_api_request(flow.request.pretty_host):
        logging.info(f'Mocking request: {flow.request.pretty_url}')

        request_json = {}
        try:
            request_json = flow.request.json()
        except json.JSONDecodeError:
            pass

        for url_substring, handler in URL_TO_MOCK_MAPPING.items():
            if url_substring in flow.request.pretty_url:
                response_content, content_type = handler(request_json)
                flow.response = http.Response.make(
                    200,
                    response_content,
                    {"Content-Type": content_type},
                )
                break
    else:
        logging.info(f'Passing through request: {flow.request.pretty_url}')
        flow.resume()
