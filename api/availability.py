from flask import Flask, request, jsonify

from api.types.availability import AvailableDateTime
from api.types.bismillah import Bismillah
from domain.repository.repo_factory import AvailabilityRepoFactory
from domain.service.availability import AvailabilityService

API = Flask(__name__)


@API.route('/user/<user_id>/availability', methods=['POST'])
def add_availabilities(user_id: str):
    raw_req = request.get_json(force=True)
    availabilities: list[AvailableDateTime] = AvailableDateTime.from_raw_req_list(raw_req)
    # No need to transform DTO to DomainModel
    try:
        existing_availabilies = AvailabilityRepoFactory.instance().get_availabilities(user_id)
        AvailabilityService.instance().validate(availabilities + existing_availabilies)
        AvailabilityRepoFactory.instance().add_availabilities(user_id, availabilities)
    except Exception as e:
        return jsonify({"error": str(e)}), 400  # Return a 400 Bad Request status for invalid data

    return {"status": "True"}, 202


@API.route('/user/<user_id>/availability', methods=['GET'])
def get_availabilities(user_id: str):
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    return jsonify(AvailabilityRepoFactory.instance().get_availabilities(user_id, start_date, end_date))


@API.route('/user/overlap', methods=['GET'])
def get_overlap():
    raw_req = request.get_json(force=True)
    user1 = raw_req.get('user1')
    user2 = raw_req.get('user2')
    data = AvailabilityRepoFactory.instance().get_overlap_intervals(user1, user2)
    return jsonify(data)
