import sys
from pathlib import Path

sys.path.append(
    str(
        Path(__file__)
        .resolve()
        .parent.parent
        / "src"
        / "lambda"
    )
)

from src.app.services.transformation_service import (
    TransformationService,
)


def test_total_amount():

    row = {
        "order_id": "1",
        "product": "Laptop",
        "quantity": "2",
        "price": "60000",
    }

    result = TransformationService.transform(
        row
    )

    assert result.total_amount == 120000