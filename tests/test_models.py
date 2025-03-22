"""Tests for the Application Models."""
from datetime import date

import pytest
from pydantic import ValidationError

from app.models.users import UserBase


@pytest.mark.unit
def test_valid_user_entry():
    UserBase(
        first_name="Jane",
        last_name="Smith",
        phone_number="987-654-3210",
        date_of_birth=date(1995, 5, 20),
        address="456 Oak Street, Lexington, KY",
        email="jane.smith@example.com",
        username="janesmith",
        password="Anothersecurepassword123&",
        user_category="admin"
    )
    assert True


@pytest.mark.unit
def test_missing_required_field():
    with pytest.raises(ValidationError) as excinfo:
        UserBase(
            last_name="Smith",
            phone_number="987-654-3210",
            date_of_birth=date(1995, 5, 20),
            address="456 Oak Street, Lexington, KY",
            email="jane.smith@example.com",
            username="janesmith",
            password="Anothersecurepassword123&",
            user_category="admin"
        )
    assert "first_name" in str(excinfo.value)


@pytest.mark.unit
def test_invalid_email_format():
    with pytest.raises(ValidationError) as excinfo:
        UserBase(
            first_name="Jane",
            last_name="Smith",
            phone_number="987-654-3210",
            date_of_birth=date(1995, 5, 20),
            address="456 Oak Street, Lexington, KY",
            email="invalid-email-format",
            username="janesmith",
            password="Anothersecurepassword123&",
            user_category="admin"
        )
    assert "email" in str(excinfo.value)


@pytest.mark.unit
def test_user_below_13_years_old():
    with pytest.raises(ValidationError) as excinfo:
        UserBase(
            first_name="Jane",
            last_name="Smith",
            phone_number="987-654-3210",
            date_of_birth=date.today().replace(year=date.today().year - 10),  # User is 10 years old
            address="456 Oak Street, Lexington, KY",
            email="jane.smith@example.com",
            username="janesmith",
            password="Anothersecurepassword123&",
            user_category="admin"
        )
    assert "date_of_birth" in str(excinfo.value)


@pytest.mark.unit
def test_user_above_13_years_old():
    user = UserBase(
        first_name="Jane",
        last_name="Smith",
        phone_number="987-654-3210",
        date_of_birth=date.today().replace(year=date.today().year - 15),  # User is 15 years old
        address="456 Oak Street, Lexington, KY",
        email="jane.smith@example.com",
        username="janesmith",
        password="Anothersecurepassword123&",
        user_category="admin"
    )
    assert user.date_of_birth == date.today().replace(year=date.today().year - 15)


@pytest.mark.unit
def test_invalid_phone_number_format():
    with pytest.raises(ValidationError) as excinfo:
        UserBase(
            first_name="Jane",
            last_name="Smith",
            phone_number="invalid-phone",
            date_of_birth=date(1995, 5, 20),
            address="456 Oak Street, Lexington, KY",
            email="jane.smith@example.com",
            username="janesmith",
            password="Anothersecurepassword123&",
            user_category="admin"
        )
    assert "phone_number" in str(excinfo.value)


@pytest.mark.unit
def test_invalid_user_entry():
    with pytest.raises(ValidationError) as excinfo:
        UserBase(
            first_name="Jane",
            last_name="Smith",
            phone_number="123456789",
            date_of_birth=date(1995, 5, 20),
            address="456 Oak Street",
            email="jane.smith@example.com",
            username="janesmith",
            password="Securepassword123+",
            user_category="admin"
        )
    assert "phone_number" in str(excinfo.value)


@pytest.mark.unit
@pytest.mark.parametrize(
    "password, expected_error",
    [
        ("Short1!", "Password must be at least 8 characters long"),
        ("lowercase1!", "Password must contain at least one uppercase letter"),
        ("UPPERCASE1!", "Password must contain at least one lowercase letter"),
        ("NoSpecial1", "Password must contain at least one special character"),
    ],
)
def test_invalid_passwords(password, expected_error):
    with pytest.raises(ValueError) as excinfo:
        UserBase.validate_password(password)
    assert expected_error in str(excinfo.value)


@pytest.mark.unit
def test_valid_password():
    valid_password = "ValidPass1!"
    assert UserBase.validate_password(valid_password) == valid_password
