# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p

if __debug__:
    try:
        from typing import Dict, List, Optional
        from typing_extensions import Literal  # noqa: F401
        EnumTypeOntologyAsset = Literal[1, 2]
    except ImportError:
        Dict, List, Optional = None, None, None  # type: ignore
        EnumTypeOntologyAsset = None  # type: ignore


class OntologyTransfer(p.MessageType):

    def __init__(
        self,
        asset: EnumTypeOntologyAsset = None,
        amount: int = None,
        from_address: str = None,
        to_address: str = None,
    ) -> None:
        self.asset = asset
        self.amount = amount
        self.from_address = from_address
        self.to_address = to_address

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('asset', p.EnumType("OntologyAsset", (1, 2)), 0),
            2: ('amount', p.UVarintType, 0),
            3: ('from_address', p.UnicodeType, 0),
            4: ('to_address', p.UnicodeType, 0),
        }