from chalicelib import localrules
from chalicelib import sb_incoming

animal = {
    "Name": "Solo",
    "DateOfBirthUtc": "2011-04-27T07:00:00Z",
    "License": {
        "Tag": "345180",
        "Issuer": {
            "Name": "City Of Escondido",
            "Uri": "/api/v2/jurisdiction/1944",
            "Id": 1944
        }
    },
    "EuthanasiaReason": None,
    "AdoptionFee": None,
    "AdoptionSummary": "2 My Personality Color Code is <b>Purple</b>; meaning I'm Happy - Go - Lucky...Carefree...Engaging...Adaptive...and Cheerful!",
    "Age": {
        "IsApproximate": False,
        "Months": 11,
        "Weeks": 1,
        "Years": 8,
        "AgeGroup": {
            "Name": "Mature Adult",
            "Id": 5
        }
    },
    "Breed": {
        "Primary": {
            "Name": "Jack Russell Terrier / Parson Russell Terrier",
            "Uri": "/api/v2/animal/species/breed/4330",
            "Id": 4330
        },
        "PrimarySpecies": {
            "Uri": "/api/v2/animal/species/115",
            "Id": 115
        },
        "Secondary": {
            "Name": "Chihuahua",
            "Uri": "/api/v2/animal/species/breed/4287",
            "Id": 4287
        },
        "SecondarySpecies": {
            "Uri": "/api/v2/animal/species/74",
            "Id": 74
        },
        "IsCrossBreed": True
    },
    "BreederRegistrationNumber": None,
    "ContactLocation": {
        "Name": "Escondido Campus",
        "Uri": "/api/v2/location/physicallocation/64",
        "Id": 64
    },
    "Features": {
        "CoatLength": None,
        "PrimaryColour": "White",
        "SecondaryColour": "Brown",
        "CoatType": None,
        "EarType": None,
        "TailType": None,
        "EyeColour": None
    },
    "Identification": {
        "HasMicrochip": False,
        "PrimaryMicrochipNumber": None,
        "PrimaryMicrochipBrand": None,
        "PrimaryMicrochipImplantDateUtc": None,
        "SecondaryMicrochipNumber": None,
        "SecondaryMicrochipBrand": None,
        "SecondaryMicrochipImplantDateUtc": None,
        "OtherIdentification": None,
        "AcoNumber": None,
        "TagColour": None,
        "CollarType": None,
        "Barcode": None,
        "ShelterTag": None,
        "CustomTag": None,
        "CollarColour": None
    },
    "Intake": {
        "DateUtc": "2019-04-27T18:39:00Z",
        "Region": {
            "Name": "Escondido Campus",
            "Uri": "/api/v2/location/physicallocation/64",
            "Id": 64
        },
        "Source": {
            "Name": "Stray",
            "Uri": "/api/v2/animal/source/14",
            "Id": 14
        },
        "ExtendedDetails": {
            "Uri": "/api/v2/animal/sourcehistory/818738",
            "Id": 818738
        },
        "Received": {
            "Name": "Fast Track",
            "Id": 1729
        },
        "SurrenderReason": None,
        "BehaviourCondition": None,
        "EmergencyBoardingReason": None
    },
    "LastUpdatedUtc": "2019-04-30T00:49:50.15Z",
    "Location": {
        "PhysicalLocation": None,
        "Kennel": None,
        "Shelter": None,
        "MostRecentPhysicalLocation": {
            "Name": "Escondido Campus",
            "Uri": "/api/v2/location/physicallocation/64",
            "Id": 64
        }
    },
    "Medical": {
        "IsDeclawed": False,
        "IsVaccinated": True,
        "SpayedNeutered": "No",
        "PreferredFood": None,
        "PreviousMedicalDetails": None
    },
    "Owner": {
        "Name": "Wesley Haid",
        "Uri": "/api/v2/person/427517",
        "Id": 427517
    },
    "Pattern": None,
    "Sex": {
        "Name": "Male",
        "Uri": "/api/v2/animal/gender/1",
        "Id": 1
    },
    "Size": None,
    "Status": {
        "DateUtc": "2019-04-30T00:45:00Z",
        "Name": "Awaiting Triage",
        "Uri": "/api/v2/animal/status/16",
        "Id": 16
    },
    "SubStatus": None,
    "SubStatuses": [],
    "Type": {
        "Name": "Dog",
        "Uri": "/api/v2/animal/species/type/3",
        "Id": 3
    },
    "AvailableForAdoptionDateUtc": "1900-01-01T00:00:00Z",
    "DateOfWeighingUtc": "2019-04-27T07:00:00Z",
    "CurrentRabiesVaccination": {
        "Name": "Rabies",
        "Uri": "/api/v2/animal/treatment/2009619",
        "Id": 2009619
    },
    "Litters": None,
    "RabiesTag": None,
    "Origin": None,
    "DangerousAnimalInformation": None,
    "LostFoundAddress": {
        "Country": {
            "Name": "United States",
            "Uri": "/api/v2/location/country/1",
            "Id": 1
        },
        "Jurisdiction": {
            "Name": "City Of Escondido",
            "Uri": "/api/v2/jurisdiction/1944",
            "Id": 1944
        },
        "State": {
            "Abbreviation": "CA",
            "Name": "California",
            "Uri": "/api/v2/location/state/55",
            "Id": 55
        },
        "StreetType": {
            "Name": "Street",
            "Uri": "/api/v2/location/streetType/2",
            "Id": 2
        },
        "Suburb": {
            "Name": "Escondido",
            "Uri": "/api/v2/location/suburb/133291",
            "Id": 133291
        },
        "DeliveryType": None,
        "PrintableString": "N Beech Street, Escondido, CA, 92025, United States",
        "PrintableStreetAddressString": "N Beech Street, Escondido, CA, 92025, United States",
        "CrossStreet": "Valley Parkway",
        "DirectionOne": "N",
        "DirectionTwo": "",
        "ExtraAddressDetails": "",
        "Postcode": "92025",
        "PostcodeSuffix": None,
        "StreetName": "Beech",
        "StreetNumber": "",
        "UnitNumber": "",
        "DeliveryNumber": "",
        "IsApiValidated": False,
        "Id": 3436765
    },
    "DateFoundUtc": "2019-04-27T07:00:00Z",
    "DateLostUtc": "2019-04-29T07:00:00Z",
    "IsDeleted": False,
    "Icons": None,
    "Weight": "14 lbs",
    "MetaData": [],
    "RelatedAnimals": None,
    "Behaviour": None,
    "Media": None,
    "DistinguishingFeatures": "My shelter name is Diego!",
    "DueDateOutUtc": "2019-05-01T07:00:00Z",
    "Id": 589800
}

animal['Id'] = 1
animal['LastUpdatedUtc'] = '2020-01-01T00:00:00Z'

localrules.triageForWeb(animal) # normally done in sb_sync.action() before handoff to incoming()

sb_incoming.process(animal)
