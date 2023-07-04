from unittest.mock import Mock, patch

import pytest

from src.main.user.domain.exceptions.UserNotFoundException import UserNotFoundException
from src.main.user.usecase.GetUserByIdUseCase import GetUserByIdUseCase
from src.tests.user.domain.port.command.UserCommandMother import UserCommandMother


@pytest.fixture
def repository():
    with patch(
        "src.main.user.usecase.GetUserByIdUseCase.InMemoryUserRepository"
    ) as mock_repository:
        mock_repository.return_value = mock_repository
        mock_repository.fetch.return_value = None
        yield mock_repository


def test_GetUserWhenExist(repository: Mock):
    usecase = GetUserByIdUseCase()
    command = UserCommandMother().companyCommand()
    repository.fetch.return_value = command.toDomain()
    response = usecase.execute(command.id)
    assert response == command.toDomain()


def test_ThrowWhenUserNoExist(repository: Mock):
    usecase = GetUserByIdUseCase()
    command = UserCommandMother().companyCommand()
    try:
        usecase.execute(command.id)
        assert False
    except UserNotFoundException:
        assert True
