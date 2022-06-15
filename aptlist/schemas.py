# cookbook/schema.py
import graphene, logging
from django.utils import timezone
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from aptlist.models import Apartment, Lease
from kafka_logger.handlers import KafkaLoggingHandler



logger = logging.getLogger("rentsite")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(threadName)-10s %(message)s')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
KAFKA_BOOTSTRAP_SERVER = ('kafka:9092')
TOPIC = 'rentsite-logger'

kh = KafkaLoggingHandler(KAFKA_BOOTSTRAP_SERVER,
                                        TOPIC,security_protocol="PLAINTEXT")
logger.addHandler(kh)


class ApartmentType(DjangoObjectType):
     class Meta:
        model = Apartment
        fields = ("id", "address", "unit_number",
                  "rent", "date_built")


class LeaseType(DjangoObjectType):
    class Meta:
        model = Lease
        fields = ("id", "apartment", "name", "lease_expires")


class ApartmentMutation(graphene.Mutation):

    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID()
        address = graphene.String(required=True)
        unit = graphene.Int(required=True)
        rent = graphene.Int(required=True)
        date_built = graphene.DateTime(required=False)
    apartment = graphene.Field(ApartmentType)

    @classmethod
    def mutate(cls, root, info, address, unit, rent, **kwargs):
        date_built = kwargs.get('date_built',timezone.now())

        apartment = Apartment(address=address, unit_number=unit,
                              rent=rent, date_built=date_built)
        apartment.save()
        # Notice we return an instance of this mutation
        return ApartmentMutation(
            apartment=apartment
        )
class UpdateRentMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID()
        rent = graphene.Int(required=True)

    apartment = graphene.Field(ApartmentType)

    @classmethod
    def mutate(cls, root, info, id, rent, **kwargs):
        logger.info("ID: {0}".format(id))
        apartment = Apartment.objects.get(id=id)
        apartment.rent=rent
        apartment.save()
        # Notice we return an instance of this mutation
        return UpdateRentMutation(
            apartment=apartment
        )


class LeaseMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        lease_expires = graphene.DateTime(required=False)
        apartment_id = graphene.Int(required=True)
        name = graphene.String(required=True)

    lease = graphene.Field(LeaseType)

    @classmethod
    def mutate(cls, root, info, apartment_id, name):
        expires = timezone.now()+timezone.timedelta(minutes=1)
        apartment = Apartment.objects.get(id=apartment_id)
        if Lease.objects.filter(apartment=apartment,  lease_expires__gt=timezone.now()).count() > 0:
            raise GraphQLError("Apartment already booked!")
        lease = Lease(apartment=apartment, name=name,lease_expires=expires)
        lease.save()
        return(LeaseMutation(lease))


class Mutation(graphene.ObjectType):
    create_apartment = ApartmentMutation.Field()
    create_lease = LeaseMutation.Field()
    update_rent = UpdateRentMutation.Field()


class Query(graphene.ObjectType):
    all_leases = graphene.List(LeaseType)
    # apartements_by_rent = graphene.String(
    #     name=graphene.String(default_value="stranger"))

    apartments_by_rent = graphene.List(ApartmentType, min_rent=graphene.Int(
        required=True), max_rent=graphene.Int(required=True))

    def resolve_all_leases(root, info):
        # We can easily optimize query count in the resolve method
        return Lease.objects.select_related("apartment").all()

    def resolve_apartments_by_rent(root, info, min_rent, max_rent):
        try:
            apartments = Apartment.objects.filter(rent__range=(min_rent, max_rent)).exclude(id__in=Lease.objects.filter(lease_expires__gt=timezone.now()).values_list('apartment_id', flat=True))
            size = len(apartments)
            logger.info("Search for apartments with rent between {0} and {1} returned {2} hits".format(min_rent,max_rent,size))
            return apartments
        except Apartment.DoesNotExist:
            return None


schema = graphene.Schema(query=Query, mutation=Mutation)
