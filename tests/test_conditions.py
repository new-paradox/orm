from orm.orm_core.Conditions import QFilter
import pytest

RESPONSE_1 = QFilter().q_select().add_v('name').q_from().add_k('users').q_where().add_k('id').eq().add_v(
    5).q_or().add_k(
    'last_name').ne().add_v('Turner').condition
RESPONSE_2 = QFilter().q_select().add_v('name').q_from().add_k('users').q_where().add_k('id').q_in().open_sh().add_v(
    3).comma().add_v(5).close_sh().q_or().add_k('last_name').ne().add_v('Turner').condition
RESPONSE_3 = QFilter().add_k('description').eq().add_v('foo').q_or().add_k('id').ne().add_v(1).condition
RESPONSE_4 = QFilter().add_k('id').lt().add_v(5).q_and().add_k('id').gt().add_v(2).condition
RESPONSE_5 = QFilter().add_k('id').le().add_v(5).q_or().add_k('id').ge().add_v(1).condition

ANSWER_1 = " SELECT 'name' FROM users WHERE id = 5 OR last_name != 'Turner'"
ANSWER_2 = " SELECT 'name' FROM users WHERE id IN (3, 5) OR last_name != 'Turner'"
ANSWER_3 = "description = 'foo' OR id != 1"
ANSWER_4 = "id < 5 AND id > 2"
ANSWER_5 = "id <= 5 OR id >= 1"


@pytest.mark.parametrize('response, answer', [
    (RESPONSE_1, ANSWER_1),
    (RESPONSE_2, ANSWER_2),
    (RESPONSE_3, ANSWER_3),
    (RESPONSE_4, ANSWER_4),
    (RESPONSE_5, ANSWER_5),
])
def test_fill_cards_from_field(response, answer):
    result = response
    assert result == answer


if __name__ == "__main__":
    pytest.main()
