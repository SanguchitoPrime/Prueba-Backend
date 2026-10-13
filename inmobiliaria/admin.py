from django.contrib import admin
from .models import Comuna, Propiedad


class PropiedadInline(admin.TabularInline):
  model = Propiedad
  extra = 1


@admin.register(Comuna)
class ComunaAdmin(admin.ModelAdmin):
  list_display = (
      "nombre",
      "region",
      "codigo_clasificacion",
      "activa",
      "total_propiedades_asociadas",
  )
  search_fields = ("nombre", "region", "codigo_clasificacion")
  list_filter = ("activa", "region")
  inlines = [PropiedadInline]

  # Metodo Calculador
  @admin.display(description="Total Propiedades")
  def total_propiedades_asociadas(self, obj):
    return obj.propiedades.count()


@admin.register(Propiedad)
class PropiedadAdmin(admin.ModelAdmin):
  list_display = (
      "codigo_propiedad",
      "direccion",
      "tipo_propiedad",
      "precio_arriendo",
      "disponible",
      "comuna",
  )
  search_fields = (
      "codigo_propiedad",
      "direccion",
      "comuna__nombre",
      "comuna__codigo_clasificacion",
  )
  list_filter = (
      "disponible",
      "tipo_propiedad",
      "comuna",
      "comuna__codigo_clasificacion",
  )
  list_editable = ("disponible", "precio_arriendo")

  # Marcar como Disponible
  @admin.action(description="Marcar propiedades seleccionadas como Disponibles")
  def marcar_disponible(self, request, queryset):
    updated = queryset.update(disponible=True)
    self.message_user(
        request,
        f"Se han marcado exitosamente {updated} propiedades como disponibles.",
    )

  # Marcar como Arrendado
  @admin.action(description="Marcar propiedades seleccionadas como Arrendadas")
  def marcar_arrendado(self, request, queryset):
    updated = queryset.update(disponible=False)
    self.message_user(
        request,
        (
            f"Se han marcado exitosamente {updated} propiedades como"
            " arrendadas."
        ),
    )

  actions = ["marcar_disponible", "marcar_arrendado"]