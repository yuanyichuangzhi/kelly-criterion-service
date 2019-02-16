from datetime import datetime
import logging

from kelly_criterion import calc_kelly_leverages
from marshmallow.exceptions import ValidationError
from flasgger import SwaggerView, Schema, fields
from flask import Response, request, make_response, jsonify

log = logging.getLogger(__name__)


def _validate_date(input_date: str) -> bool:
    try:
        datetime.strptime(input_date, "%Y-%m-%d")
        return True
    except ValueError:
        return False


class KellyCriterionRequest(Schema):  # type: ignore
    start_date = fields.Str(
        description='Start date',
        example='2018-1-1',
        default='',
        required=True,
        validate=_validate_date)

    end_date = fields.Str(
        description='End date',
        example='2018-12-31',
        default='',
        required=True,
        validate=_validate_date)

    securities = fields.List(
        description='List of securities (stock symbols) to calculate '
                    'leverage for the given date range ',
        example=['IBM', 'AAPL'],
        default=[],
        cls_or_instance=fields.Str())

    risk_free_rate = fields.Float(
        description='Risk free rate',
        example=0.04,
        default=0.04)


class KellyCriterionResponse(Schema):  # type: ignore
    job_names = fields.List(cls_or_instance=fields.Str())


class KellyCriterionView(SwaggerView):  # type: ignore
    tags = ['kelly_criterion']
    parameters = KellyCriterionRequest
    responses = {
        200: {
            'description': "Kelly Leverages",
            'schema': KellyCriterionResponse
        },
        400: {'description': 'Error occured while serving the request.'}
    }
    validation = True

    # pylint: disable=no-self-use
    def post(self) -> Response:
        """
        Kelly Leverage calculation
        """
        try:
            params = KellyCriterionRequest().load(request.json)
            log.info(params)

            leverages = calc_kelly_leverages(
                start_date=params['start_date'],
                end_date=params['end_date'],
                securities=params['securities'],
                risk_free_rate=params['risk_free_rate'])
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

        return make_response(jsonify(leverages), 200)
