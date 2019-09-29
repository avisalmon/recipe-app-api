from rest_framework import serializers

from core.models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag object"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_Fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for the Ingredient Model"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_Fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for the Recipes."""

    ingredients = IngredientSerializer(
        many=True,
        read_only=True
    )

    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
        )

    class Meta:
        model = Recipe
        fields = ('id',
                  'title',
                  'ingredients',
                  'tags',
                  'time_minutes',
                  'price',
                  'link')

        read_only_Fields = ('id',)
