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
        description='Start date of the sampling period',
        example='2018-1-1',
        default='',
        required=True,
        validate=_validate_date)

    end_date = fields.Str(
        description='End date of the sampling period',
        example='2018-12-31',
        default='',
        required=True,
        validate=_validate_date)

    securities = fields.List(
        description='List of securities (stock symbols) to calculate '
                    'the leverage using the given sampling period.',
        example=['IBM', 'AAPL'],
        default=[],
        cls_or_instance=fields.Str())

    risk_free_rate = fields.Float(
        description='Risk free rate',
        example=0.04,
        default=0.04)


class KellyCriterionResponse(Schema):  # type: ignore
    kelly_leverages = fields.Dict(
        keys=fields.Str(description='Security'),
        values=fields.Float(description='Optimal Kelly Leverage'))


class KellyCriterionView(SwaggerView):  # type: ignore
    summary = "Kelly Criterion for Stock Market"
    description = """
    Money management strategy based on Kelly J. L.'s formula described in 
    "A New Interpretation of Information Rate". 
    The formula was adopted to gambling and stock market by Ed Thorp, et al., 
    see: The Kelly Criterion in Blackjack Sports Betting, and the Stock Market.

    This service calculates the optimal capital allocation for the provided 
    portfolio of securities with the formula:
        f_i = m_i / s_i^2
    where
        * f_i is the calculated leverage of the i-th security of the portfolio
        * m_i is the mean of the return of the i-th security
        * s_i is the standard deviation of the return of the i-th security
    assuming that the strategies for the securities are all statistically 
    independent.

    The stock quotes are downloaded from IEX Exchange. 
    
    Reference (Matlab) implementation was taken from Ernie Chan's 
    Quantitative Trading book (ISBN 978-0470284889).
    """
    tags = ['kelly_criterion']
    parameters = KellyCriterionRequest
    responses = {
        200: {
            'description': "Optimal leverages based on Kelly's Criterion",
            'schema': KellyCriterionResponse
        },
        400: {'description': 'Error occurred while serving the request.'}
    }
    validation = True

    # pylint: disable=no-self-use
    def post(self) -> Response:
        """
        Optimal leverage calculation using Kelly Criterion
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
