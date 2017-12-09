from flask import Flask
from .database import db
from .models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


def main():
    adam = Profile(first_name="Adam", last_name="Scott")
    maude = Profile(first_name="Maude", last_name="Benoit-Charbonneau")

    adam_email = ProfileEmail(email="ascott.ca@gmail.com")
    maude_email = ProfileEmail(email="maude.benoit-charbonneau@hotmail.com")
    maude_email_alt = ProfileEmail(email="maude.benoit-charbonneau@usherbrooke.ca")

    adam.emails.append(adam_email)
    maude.emails.append(maude_email)
    maude.emails.append(maude_email_alt)

    print(adam.emails, maude.emails)

    type_adresse_maison = ProfileAddressType(address_type=ProfileAddressTypeEnum.HOME)

    adam_adresse = ProfileAddress(
        address_1="150, rue des Pins",
        city="Sainte-Sabine",
        state="Québec",
        country="Canada",
        postal_code="J0J 2B0",
        address_type=type_adresse_maison
    )
    maude_adresse = ProfileAddress(
        address_1="463, rue Galt Ouest",
        city="Sherbrooke",
        state="Québec",
        country="Canada",
        postal_code="J1H 1Y5",
        address_type=type_adresse_maison
    )

    adam.addresses.append(adam_adresse)
    maude.addresses.append(maude_adresse)

    print(adam.addresses, maude.addresses)

    case = Case(files=[
        File(file_number="450-12-012345-179")
    ])

    print(case)

    with app.app_context():
        db.create_all()

        db.session.add(adam)
        db.session.add(maude)
        db.session.add(case)
        db.session.commit()

        maude_query = db.session.query(Profile).filter_by(first_name="Maude").one()

        adam_query = db.session.query(ProfileAddress).filter(
            ProfileAddress.profile.has(Profile.first_name=="Adam")
        ).one()
        print(maude_query, adam_query)

        case_query = db.session.query(File).filter(File.file_number=="450-12-012345-179").one().case
        print(case_query)


if __name__ == "__main__":
    main()
