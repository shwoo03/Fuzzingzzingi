import json
import urllib.parse

def save_packet_to_json(packet_storage, output_file='packets.json'):
    packets = []
    for raw_data in packet_storage:
        try:
            request_line, headers_alone = raw_data.split(b'\r\n', 1)
            headers, body = headers_alone.split(b'\r\n\r\n', 1)
        except ValueError:
            continue

        request_line = request_line.decode('iso-8859-1')
        headers = headers.decode('iso-8859-1')
        body = body.decode('iso-8859-1')

        request_parts = request_line.split()
        if len(request_parts) < 3:
            continue

        method, url, version = request_parts
        parsed_url = urllib.parse.urlsplit(url)
        params = urllib.parse.parse_qs(parsed_url.query)
        
        headers_dict = {}
        for header_line in headers.split('\r\n'):
            key, value = header_line.split(': ', 1)
            headers_dict[key] = value
        
        cookies = headers_dict.get('Cookie', '')
        cookies_dict = urllib.parse.parse_qs(cookies.replace('; ', '&'))

        packet_info = {
            'url': url,
            'parameters': params,
            'method': method,
            'protocol_version': version,
            'headers': headers_dict,
            'cookies': cookies_dict,
            'response_body': body
        }

        packets.append(packet_info)

    with open(output_file, 'w') as f:
        json.dump(packets, f, indent=4)

    print(f"Packets saved to {output_file}")
