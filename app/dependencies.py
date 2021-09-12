import hashlib
import io
import os
import uuid
from functools import lru_cache
from pathlib import Path

import xmltodict
from fastapi import Depends
from pydantic import BaseModel

from .config import Settings


class CheckInfoBasesResponse(BaseModel):
    InfoBasesChanged: bool = False
    URL: str
    location: str

    def envelope(self) -> str:
        envelope = f"""
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
            <m:CheckInfoBasesResponse xmlns:m="{self.location}/WebCommonInfoBases">
                <m:return xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
                <m:InfoBasesChanged xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">{self.InfoBasesChanged}</m:InfoBasesChanged>
                <m:URL xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">{self.URL}</m:URL>
            </m:CheckInfoBasesResponse>
        </soap:Body>
        </soap:Envelope>
        """
        return envelope


class GetInfoBasesResponse(BaseModel):
    ClientID: str = "00000000-0000-0000-0000-000000000000"
    InfoBasesCheckCode: str = "00000000-0000-0000-0000-000000000000"
    InfoBases: str = "0"
    location: str

    def envelope(self) -> str:
        envelope = f"""
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
            <m:GetInfoBasesResponse xmlns:m="{self.location}/WebCommonInfoBases">
                <m:return xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
                <m:ClientID xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">{self.ClientID}</m:ClientID>
                <m:InfoBasesCheckCode xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">{self.InfoBasesCheckCode}</m:InfoBasesCheckCode>
                <m:InfoBases xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">{self.InfoBases}</m:InfoBases>
            </m:GetInfoBasesResponse>
        </soap:Body>
        </soap:Envelope>
        """
        return envelope


class SoapRequest:
    ...
    # TODO парсер запроса


class InfoBasesList:
    def __init__(self, content):
        self.content: str = content
        hash_object = hashlib.md5(self.content.encode())
        self.md5_hash: str = hash_object.hexdigest()


class InfoBasesCatalog:
    def __init__(self):
        self._name_index = {}
        self._infobases = []

    def add_from_file(self, file: str):
        p = Path(file)
        with open(file, encoding="utf-8") as f:
            content = f.read()
            infobases = InfoBasesList(content=content)
            self._name_index[p.stem] = infobases
            self._infobases.append(infobases)

    def get_infobases(self, name_id: str) -> InfoBasesList or None:
        return self._name_index.get(name_id, None)


def check_code():
    return str(uuid.uuid4())


def parse_xml_body(xml_body: bytes):
    b = io.BytesIO(xml_body)
    return xmltodict.parse(b)


def get_client_id() -> str:
    return "af822745-ab05-42ac-b826-80d422afb4b7"


def get_wsdl(location: str, path: str) -> str:
    wsdl = f"""<?xml version="1.0" encoding="UTF-8"?>
    <definitions xmlns="http://schemas.xmlsoap.org/wsdl/"
        xmlns:soap12bind="http://schemas.xmlsoap.org/wsdl/soap12/"
        xmlns:soapbind="http://schemas.xmlsoap.org/wsdl/soap/"
        xmlns:tns="{location}/WebCommonInfoBases"
        xmlns:wsp="http://schemas.xmlsoap.org/ws/2004/09/policy"
        xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema"
        xmlns:xsd1="{location}/WebCommonInfoBases" name="WebCommonInfoBases" targetNamespace="{location}/WebCommonInfoBases">
        <types>
            <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
                xmlns:xs1="{location}/WebCommonInfoBases" targetNamespace="{location}/WebCommonInfoBases" elementFormDefault="qualified">
                <xs:element name="CheckInfoBases">
                    <xs:complexType>
                        <xs:sequence>
                            <xs:element name="ClientID" type="xs:string" nillable="true"/>
                            <xs:element name="InfoBasesCheckCode" type="xs:string" nillable="true"/>
                        </xs:sequence>
                    </xs:complexType>
                </xs:element>
                <xs:element name="CheckInfoBasesResponse">
                    <xs:complexType>
                        <xs:sequence>
                            <xs:element name="return" type="xs:string" nillable="true"/>
                            <xs:element name="InfoBasesChanged" type="xs:boolean" nillable="true"/>
                            <xs:element name="URL" type="xs:string" nillable="true"/>
                        </xs:sequence>
                    </xs:complexType>
                </xs:element>
                <xs:element name="GetInfoBases">
                    <xs:complexType>
                        <xs:sequence>
                            <xs:element name="ClientID" type="xs:string" nillable="true"/>
                        </xs:sequence>
                    </xs:complexType>
                </xs:element>
                <xs:element name="GetInfoBasesResponse">
                    <xs:complexType>
                        <xs:sequence>
                            <xs:element name="return" type="xs:string" nillable="true"/>
                            <xs:element name="ClientID" type="xs:string" nillable="true"/>
                            <xs:element name="InfoBasesCheckCode" type="xs:string" nillable="true"/>
                            <xs:element name="InfoBases" type="xs:string" nillable="true"/>
                        </xs:sequence>
                    </xs:complexType>
                </xs:element>
            </xs:schema>
        </types>
        <message name="CheckInfoBasesRequestMessage">
            <part name="parameters" element="tns:CheckInfoBases"/>
        </message>
        <message name="CheckInfoBasesResponseMessage">
            <part name="parameters" element="tns:CheckInfoBasesResponse"/>
        </message>
        <message name="GetInfoBasesRequestMessage">
            <part name="parameters" element="tns:GetInfoBases"/>
        </message>
        <message name="GetInfoBasesResponseMessage">
            <part name="parameters" element="tns:GetInfoBasesResponse"/>
        </message>
        <portType name="WebCommonInfoBasesPortType">
            <operation name="CheckInfoBases">
                <input message="tns:CheckInfoBasesRequestMessage"/>
                <output message="tns:CheckInfoBasesResponseMessage"/>
            </operation>
            <operation name="GetInfoBases">
                <input message="tns:GetInfoBasesRequestMessage"/>
                <output message="tns:GetInfoBasesResponseMessage"/>
            </operation>
        </portType>
        <binding name="WebCommonInfoBasesSoapBinding" type="tns:WebCommonInfoBasesPortType">
            <soapbind:binding style="document" transport="http://schemas.xmlsoap.org/soap/http"/>
            <operation name="CheckInfoBases">
                <soapbind:operation style="document" soapAction="{location}/WebCommonInfoBases#WebCommonInfoBases:CheckInfoBases"/>
                <input>
                    <soapbind:body use="literal"/>
                </input>
                <output>
                    <soapbind:body use="literal"/>
                </output>
            </operation>
            <operation name="GetInfoBases">
                <soapbind:operation style="document" soapAction="{location}/WebCommonInfoBases#WebCommonInfoBases:GetInfoBases"/>
                <input>
                    <soapbind:body use="literal"/>
                </input>
                <output>
                    <soapbind:body use="literal"/>
                </output>
            </operation>
        </binding>
        <binding name="WebCommonInfoBasesSoap12Binding" type="tns:WebCommonInfoBasesPortType">
            <soap12bind:binding style="document" transport="http://schemas.xmlsoap.org/soap/http"/>
            <operation name="CheckInfoBases">
                <soap12bind:operation style="document" soapAction="{location}/WebCommonInfoBases#WebCommonInfoBases:CheckInfoBases"/>
                <input>
                    <soap12bind:body use="literal"/>
                </input>
                <output>
                    <soap12bind:body use="literal"/>
                </output>
            </operation>
            <operation name="GetInfoBases">
                <soap12bind:operation style="document" soapAction="{location}/WebCommonInfoBases#WebCommonInfoBases:GetInfoBases"/>
                <input>
                    <soap12bind:body use="literal"/>
                </input>
                <output>
                    <soap12bind:body use="literal"/>
                </output>
            </operation>
        </binding>
        <service name="WebCommonInfoBases">
            <port name="WebCommonInfoBasesSoap" binding="tns:WebCommonInfoBasesSoapBinding">
                <documentation>
                    <wsi:Claim xmlns:wsi="http://ws-i.org/schemas/conformanceClaim/" conformsTo="http://ws-i.org/profiles/basic/1.1"/>
                </documentation>
                <soapbind:address location="{location}{path}"/>
            </port>
        </service>
    </definitions>
    """
    return wsdl


def parse_infobases_catalog(v8i_catalog) -> InfoBasesCatalog:
    if not v8i_catalog or not os.path.exists(v8i_catalog):
        raise ValueError("v8i_catalog:" + str(v8i_catalog))

    catalog = InfoBasesCatalog()
    for subdir, dirs, files in os.walk(v8i_catalog):
        for file in files:
            if not file.endswith(".v8i"):
                continue
            catalog.add_from_file(os.path.join(v8i_catalog, file))

    return catalog


@lru_cache()
def get_settings() -> Settings:
    return Settings()


@lru_cache()
def get_infobases_catalog(
    settings: Settings = Depends(get_settings),
) -> InfoBasesCatalog:
    return parse_infobases_catalog(settings.v8i_folder)
