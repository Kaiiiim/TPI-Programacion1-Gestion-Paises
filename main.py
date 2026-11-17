"""Punto de entrada de la aplicación de gestión de países.

Ofrece un menú interactivo en consola que permite agregar, actualizar,
buscar, filtrar, ordenar y analizar países a partir de un dataset CSV.
"""

import os
import sys

# Asegurar entrada/salida en UTF-8 (importante en Windows)
try:
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

# Permitir ejecutar desde cualquier directorio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Cargar paises.py de forma robusta (independiente del directorio de trabajo)
import base64 as _b64
import importlib.util as _ilu
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_paises_path = os.path.join(_BASE_DIR, "paises.py")
try:
    _paises_spec = _ilu.spec_from_file_location("paises", _paises_path)
    _paises_mod = _ilu.module_from_spec(_paises_spec)
    _paises_spec.loader.exec_module(_paises_mod)
except (FileNotFoundError, ModuleNotFoundError, OSError, ImportError):
    # Fallback: paises.py no esta disponible (ej. se ejecuto solo main.py desde un zip).
    # Se usa una copia embebida del modulo para que el programa siga funcionando.
    _paises_code = _b64.b64decode("IiIiTcOzZHVsbyBjb24gbGEgbMOzZ2ljYSBkZSBnZXN0acOzbiBkZSBwYcOtc2VzLgoKQ29udGllbmUgZnVuY2lvbmVzIHBhcmEgY2FyZ2FyL2d1YXJkYXIgZWwgZGF0YXNldCwgYWdyZWdhciwgYnVzY2FyLCBmaWx0cmFyLApvcmRlbmFyIHkgY2FsY3VsYXIgZXN0YWTDrXN0aWNhcyBzb2JyZSBwYcOtc2VzLiBDYWRhIGZ1bmNpw7NuIHRpZW5lIHVuYSDDum5pY2EKcmVzcG9uc2FiaWxpZGFkIChtb2R1bGFyaXphY2nDs24pLgoiIiIKCmltcG9ydCBjc3YKaW1wb3J0IG9zCmltcG9ydCB1bmljb2RlZGF0YQpmcm9tIHR5cGluZyBpbXBvcnQgTGlzdCwgRGljdCwgT3B0aW9uYWwsIEFueQoKCiMgLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tCiMgRXN0cnVjdHVyYSBkZSBkYXRvcwojIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQojIFVuIHBhw61zIHNlIHJlcHJlc2VudGEgY29tbyB1biBkaWNjaW9uYXJpbyBjb24gbGFzIHNpZ3VpZW50ZXMgY2xhdmVzOgojICAgIm5vbWJyZSI6IHN0cgojICAgInBvYmxhY2lvbiI6IGludAojICAgInN1cGVyZmljaWUiOiBpbnQgICAoZW4ga23CsikKIyAgICJjb250aW5lbnRlIjogc3RyCiMgRWwgZGF0YXNldCBjb21wbGV0byBlcyB1bmEgbGlzdGEgZGUgZXN0b3MgZGljY2lvbmFyaW9zLgoKCkNBTVBPU19PQkxJR0FUT1JJT1MgPSAoIm5vbWJyZSIsICJwb2JsYWNpb24iLCAic3VwZXJmaWNpZSIsICJjb250aW5lbnRlIikKCgojIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQojIE5vcm1hbGl6YWNpw7NuIGRlIHRleHRvCiMgLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tCgpkZWYgbm9ybWFsaXphcl90ZXh0byh0ZXh0bzogc3RyKSAtPiBzdHI6CiAgICAiIiJOb3JtYWxpemEgdW4gdGV4dG86IGxvIHBhc2EgYSBtaW7DunNjdWxhcyB5IHF1aXRhIHRpbGRlcy9kaWFjcsOtdGljb3MuCgogICAgw5p0aWwgcGFyYSBjb21wYXJhY2lvbmVzIGluc2Vuc2libGVzIGEgbWF5w7pzY3VsYXMgeSBhY2VudG9zLgogICAgIiIiCiAgICBpZiB0ZXh0byBpcyBOb25lOgogICAgICAgIHJldHVybiAiIgogICAgdGV4dG8gPSBzdHIodGV4dG8pLmxvd2VyKCkKICAgICMgRGVzY29tcG9uZSBjYXJhY3RlcmVzIGFjZW50dWFkb3MgKE5GRCkgeSBlbGltaW5hIGxhcyBtYXJjYXMgZGlhY3LDrXRpY2FzCiAgICB0ZXh0byA9IHVuaWNvZGVkYXRhLm5vcm1hbGl6ZSgiTkZEIiwgdGV4dG8pCiAgICB0ZXh0byA9ICIiLmpvaW4oYyBmb3IgYyBpbiB0ZXh0byBpZiB1bmljb2RlZGF0YS5jYXRlZ29yeShjKSAhPSAiTW4iKQogICAgcmV0dXJuIHRleHRvCgoKIyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0KIyBWYWxpZGFjaW9uZXMKIyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0KCmRlZiB2YWxpZGFyX25vX3ZhY2lvKHRleHRvOiBzdHIsIGNhbXBvOiBzdHIgPSAidmFsb3IiKSAtPiBzdHI6CiAgICAiIiJWYWxpZGEgcXVlIHVuIHRleHRvIG5vIGVzdMOpIHZhY8OtbyAobmkgc29sbyBlc3BhY2lvcykuCgogICAgTGFuemEgVmFsdWVFcnJvciBzaSBlbCB0ZXh0byBlcyB2YWPDrW8uCiAgICAiIiIKICAgIGlmIHRleHRvIGlzIE5vbmU6CiAgICAgICAgcmFpc2UgVmFsdWVFcnJvcihmIkVsIGNhbXBvICd7Y2FtcG99JyBubyBwdWVkZSBlc3RhciB2YWPDrW8uIikKICAgIHRleHRvID0gdGV4dG8uc3RyaXAoKQogICAgaWYgdGV4dG8gPT0gIiI6CiAgICAgICAgcmFpc2UgVmFsdWVFcnJvcihmIkVsIGNhbXBvICd7Y2FtcG99JyBubyBwdWVkZSBlc3RhciB2YWPDrW8uIikKICAgIHJldHVybiB0ZXh0bwoKCmRlZiB2YWxpZGFyX2VudGVyb19wb3NpdGl2byh2YWxvcjogQW55LCBjYW1wbzogc3RyID0gInZhbG9yIikgLT4gaW50OgogICAgIiIiVmFsaWRhIHkgY29udmllcnRlIHVuIHZhbG9yIGEgZW50ZXJvIHBvc2l0aXZvLgoKICAgIEFjZXB0YSBzdHIgbyBpbnQuIExhbnphIFZhbHVlRXJyb3Igc2kgbm8gZXMgdW4gZW50ZXJvIHbDoWxpZG8gbyBubyBlcyBwb3NpdGl2by4KICAgICIiIgogICAgaWYgaXNpbnN0YW5jZSh2YWxvciwgYm9vbCk6CiAgICAgICAgcmFpc2UgVmFsdWVFcnJvcihmIkVsIGNhbXBvICd7Y2FtcG99JyBkZWJlIHNlciB1biBuw7ptZXJvIGVudGVyby4iKQogICAgaWYgaXNpbnN0YW5jZSh2YWxvciwgaW50KToKICAgICAgICBudW1lcm8gPSB2YWxvcgogICAgZWxzZToKICAgICAgICB0ZXh0byA9IHN0cih2YWxvcikuc3RyaXAoKQogICAgICAgIGlmIHRleHRvID09ICIiOgogICAgICAgICAgICByYWlzZSBWYWx1ZUVycm9yKGYiRWwgY2FtcG8gJ3tjYW1wb30nIG5vIHB1ZWRlIGVzdGFyIHZhY8Otby4iKQogICAgICAgIHRyeToKICAgICAgICAgICAgbnVtZXJvID0gaW50KHRleHRvKQogICAgICAgIGV4Y2VwdCAoVmFsdWVFcnJvciwgVHlwZUVycm9yKToKICAgICAgICAgICAgcmFpc2UgVmFsdWVFcnJvcihmIkVsIGNhbXBvICd7Y2FtcG99JyBkZWJlIHNlciB1biBuw7ptZXJvIGVudGVyby4iKQogICAgaWYgbnVtZXJvIDw9IDA6CiAgICAgICAgcmFpc2UgVmFsdWVFcnJvcihmIkVsIGNhbXBvICd7Y2FtcG99JyBkZWJlIHNlciBtYXlvciBxdWUgY2Vyby4iKQogICAgcmV0dXJuIG51bWVybwoKCiMgLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tCiMgUGVyc2lzdGVuY2lhIChDU1YpCiMgLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tCgpkZWYgY2FyZ2FyX3BhaXNlcyhydXRhOiBzdHIpIC0+IExpc3RbRGljdF06CiAgICAiIiJDYXJnYSBlbCBkYXRhc2V0IGRlIHBhw61zZXMgZGVzZGUgdW4gYXJjaGl2byBDU1YuCgogICAgRGV2dWVsdmUgdW5hIGxpc3RhIGRlIGRpY2Npb25hcmlvcy4gU2kgZWwgYXJjaGl2byBubyBleGlzdGUgbyB0aWVuZQogICAgZXJyb3JlcyBkZSBmb3JtYXRvLCBzZSBtYW5lamFuIGRlIGZvcm1hIGNvbnRyb2xhZGEgeSBzZSBkZXZ1ZWx2ZSBsYQogICAgbGlzdGEgKHBvc2libGVtZW50ZSB2YWPDrWEpIGp1bnRvIGNvbiB1biBtZW5zYWplIGRlIGFkdmVydGVuY2lhLgogICAgIiIiCiAgICBwYWlzZXM6IExpc3RbRGljdF0gPSBbXQogICAgaWYgbm90IG9zLnBhdGguZXhpc3RzKHJ1dGEpOgogICAgICAgIHByaW50KGYiQWR2ZXJ0ZW5jaWE6IGVsIGFyY2hpdm8gJ3tydXRhfScgbm8gZXhpc3RlLiBTZSBpbmljaWEgY29uIGRhdGFzZXQgdmFjw61vLiIpCiAgICAgICAgcmV0dXJuIHBhaXNlcwoKICAgIHRyeToKICAgICAgICB3aXRoIG9wZW4ocnV0YSwgbW9kZT0iciIsIGVuY29kaW5nPSJ1dGYtOCIsIG5ld2xpbmU9IiIpIGFzIGFyY2hpdm86CiAgICAgICAgICAgIGxlY3RvciA9IGNzdi5EaWN0UmVhZGVyKGFyY2hpdm8pCiAgICAgICAgICAgIGlmIGxlY3Rvci5maWVsZG5hbWVzIGlzIE5vbmU6CiAgICAgICAgICAgICAgICBwcmludCgiQWR2ZXJ0ZW5jaWE6IGVsIENTViBubyB0aWVuZSBlbmNhYmV6YWRvLiBTZSBpbmljaWEgY29uIGRhdGFzZXQgdmFjw61vLiIpCiAgICAgICAgICAgICAgICByZXR1cm4gcGFpc2VzCgogICAgICAgICAgICAjIE5vcm1hbGl6YXIgbm9tYnJlcyBkZSBjb2x1bW5hcyAobWluw7pzY3VsYXMgeSBzaW4gZXNwYWNpb3MpCiAgICAgICAgICAgIGNhbXBvcyA9IFtjLnN0cmlwKCkubG93ZXIoKSBmb3IgYyBpbiBsZWN0b3IuZmllbGRuYW1lc10KICAgICAgICAgICAgZm9yIGNhbXBvIGluIENBTVBPU19PQkxJR0FUT1JJT1M6CiAgICAgICAgICAgICAgICBpZiBjYW1wbyBub3QgaW4gY2FtcG9zOgogICAgICAgICAgICAgICAgICAgIHByaW50KGYiQWR2ZXJ0ZW5jaWE6IGZhbHRhIGxhIGNvbHVtbmEgJ3tjYW1wb30nIGVuIGVsIENTVi4gU2UgaW5pY2lhIGNvbiBkYXRhc2V0IHZhY8Otby4iKQogICAgICAgICAgICAgICAgICAgIHJldHVybiBwYWlzZXMKCiAgICAgICAgICAgIGZvciBudW1lcm9fZmlsYSwgZmlsYSBpbiBlbnVtZXJhdGUobGVjdG9yLCBzdGFydD0yKToKICAgICAgICAgICAgICAgIHRyeToKICAgICAgICAgICAgICAgICAgICBub21icmUgPSB2YWxpZGFyX25vX3ZhY2lvKGZpbGEuZ2V0KCJub21icmUiLCAiIiksICJub21icmUiKQogICAgICAgICAgICAgICAgICAgIHBvYmxhY2lvbiA9IHZhbGlkYXJfZW50ZXJvX3Bvc2l0aXZvKGZpbGEuZ2V0KCJwb2JsYWNpb24iLCAiIiksICJwb2JsYWNpb24iKQogICAgICAgICAgICAgICAgICAgIHN1cGVyZmljaWUgPSB2YWxpZGFyX2VudGVyb19wb3NpdGl2byhmaWxhLmdldCgic3VwZXJmaWNpZSIsICIiKSwgInN1cGVyZmljaWUiKQogICAgICAgICAgICAgICAgICAgIGNvbnRpbmVudGUgPSB2YWxpZGFyX25vX3ZhY2lvKGZpbGEuZ2V0KCJjb250aW5lbnRlIiwgIiIpLCAiY29udGluZW50ZSIpCiAgICAgICAgICAgICAgICBleGNlcHQgVmFsdWVFcnJvciBhcyBlOgogICAgICAgICAgICAgICAgICAgIHByaW50KGYiRmlsYSB7bnVtZXJvX2ZpbGF9IGlnbm9yYWRhIHBvciBlcnJvciBkZSBmb3JtYXRvOiB7ZX0iKQogICAgICAgICAgICAgICAgICAgIGNvbnRpbnVlCiAgICAgICAgICAgICAgICBwYWlzZXMuYXBwZW5kKHsKICAgICAgICAgICAgICAgICAgICAibm9tYnJlIjogbm9tYnJlLAogICAgICAgICAgICAgICAgICAgICJwb2JsYWNpb24iOiBwb2JsYWNpb24sCiAgICAgICAgICAgICAgICAgICAgInN1cGVyZmljaWUiOiBzdXBlcmZpY2llLAogICAgICAgICAgICAgICAgICAgICJjb250aW5lbnRlIjogY29udGluZW50ZSwKICAgICAgICAgICAgICAgIH0pCiAgICBleGNlcHQgKE9TRXJyb3IsIGNzdi5FcnJvcikgYXMgZToKICAgICAgICBwcmludChmIkVycm9yIGFsIGxlZXIgZWwgYXJjaGl2byBDU1Y6IHtlfSIpCgogICAgcmV0dXJuIHBhaXNlcwoKCmRlZiBndWFyZGFyX3BhaXNlcyhydXRhOiBzdHIsIHBhaXNlczogTGlzdFtEaWN0XSkgLT4gYm9vbDoKICAgICIiIkd1YXJkYSBsYSBsaXN0YSBkZSBwYcOtc2VzIGVuIHVuIGFyY2hpdm8gQ1NWLgoKICAgIERldnVlbHZlIFRydWUgc2kgc2UgZ3VhcmTDsyBjb3JyZWN0YW1lbnRlLCBGYWxzZSBlbiBjYXNvIGRlIGVycm9yLgogICAgIiIiCiAgICB0cnk6CiAgICAgICAgb3MubWFrZWRpcnMob3MucGF0aC5kaXJuYW1lKHJ1dGEpIG9yICIuIiwgZXhpc3Rfb2s9VHJ1ZSkKICAgICAgICB3aXRoIG9wZW4ocnV0YSwgbW9kZT0idyIsIGVuY29kaW5nPSJ1dGYtOCIsIG5ld2xpbmU9IiIpIGFzIGFyY2hpdm86CiAgICAgICAgICAgIGVzY3JpdG9yID0gY3N2LkRpY3RXcml0ZXIoYXJjaGl2bywgZmllbGRuYW1lcz1saXN0KENBTVBPU19PQkxJR0FUT1JJT1MpKQogICAgICAgICAgICBlc2NyaXRvci53cml0ZWhlYWRlcigpCiAgICAgICAgICAgIGZvciBwYWlzIGluIHBhaXNlczoKICAgICAgICAgICAgICAgIGVzY3JpdG9yLndyaXRlcm93KHBhaXMpCiAgICAgICAgcmV0dXJuIFRydWUKICAgIGV4Y2VwdCAoT1NFcnJvciwgY3N2LkVycm9yKSBhcyBlOgogICAgICAgIHByaW50KGYiRXJyb3IgYWwgZ3VhcmRhciBlbCBhcmNoaXZvIENTVjoge2V9IikKICAgICAgICByZXR1cm4gRmFsc2UKCgojIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQojIENyZWFjacOzbiB5IG1vZGlmaWNhY2nDs24KIyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0KCmRlZiBjcmVhcl9wYWlzKG5vbWJyZTogc3RyLCBwb2JsYWNpb246IEFueSwgc3VwZXJmaWNpZTogQW55LCBjb250aW5lbnRlOiBzdHIpIC0+IERpY3Q6CiAgICAiIiJDcmVhIHkgdmFsaWRhIHVuIGRpY2Npb25hcmlvIHF1ZSByZXByZXNlbnRhIHVuIHBhw61zLiIiIgogICAgcmV0dXJuIHsKICAgICAgICAibm9tYnJlIjogdmFsaWRhcl9ub192YWNpbyhub21icmUsICJub21icmUiKSwKICAgICAgICAicG9ibGFjaW9uIjogdmFsaWRhcl9lbnRlcm9fcG9zaXRpdm8ocG9ibGFjaW9uLCAicG9ibGFjaW9uIiksCiAgICAgICAgInN1cGVyZmljaWUiOiB2YWxpZGFyX2VudGVyb19wb3NpdGl2byhzdXBlcmZpY2llLCAic3VwZXJmaWNpZSIpLAogICAgICAgICJjb250aW5lbnRlIjogdmFsaWRhcl9ub192YWNpbyhjb250aW5lbnRlLCAiY29udGluZW50ZSIpLAogICAgfQoKCmRlZiBhZ3JlZ2FyX3BhaXMocGFpc2VzOiBMaXN0W0RpY3RdLCBwYWlzOiBEaWN0KSAtPiBib29sOgogICAgIiIiQWdyZWdhIHVuIHBhw61zIGEgbGEgbGlzdGEgc2kgbm8gZXhpc3RlIG90cm8gY29uIGVsIG1pc21vIG5vbWJyZS4KCiAgICBMYSBjb21wYXJhY2nDs24gZGUgbm9tYnJlcyBlcyBjYXNlLWluc2Vuc2l0aXZlLiBEZXZ1ZWx2ZSBUcnVlIHNpIHNlIGFncmVnw7MuCiAgICAiIiIKICAgIG5vbWJyZV9udWV2byA9IHBhaXNbIm5vbWJyZSJdLmxvd2VyKCkKICAgIGZvciBleGlzdGVudGUgaW4gcGFpc2VzOgogICAgICAgIGlmIGV4aXN0ZW50ZVsibm9tYnJlIl0ubG93ZXIoKSA9PSBub21icmVfbnVldm86CiAgICAgICAgICAgIHByaW50KGYiWWEgZXhpc3RlIHVuIHBhw61zIGNvbiBlbCBub21icmUgJ3twYWlzWydub21icmUnXX0nLiIpCiAgICAgICAgICAgIHJldHVybiBGYWxzZQogICAgcGFpc2VzLmFwcGVuZChwYWlzKQogICAgcmV0dXJuIFRydWUKCgpkZWYgYWN0dWFsaXphcl9wYWlzKHBhaXNlczogTGlzdFtEaWN0XSwgbm9tYnJlOiBzdHIsCiAgICAgICAgICAgICAgICAgICAgcG9ibGFjaW9uOiBPcHRpb25hbFtBbnldID0gTm9uZSwKICAgICAgICAgICAgICAgICAgICBzdXBlcmZpY2llOiBPcHRpb25hbFtBbnldID0gTm9uZSkgLT4gYm9vbDoKICAgICIiIkFjdHVhbGl6YSBsYSBwb2JsYWNpw7NuIHkvbyBzdXBlcmZpY2llIGRlIHVuIHBhw61zIGV4aXN0ZW50ZS4KCiAgICBEZXZ1ZWx2ZSBUcnVlIHNpIHNlIGFjdHVhbGl6w7MsIEZhbHNlIHNpIG5vIHNlIGVuY29udHLDsyBlbCBwYcOtcy4KICAgICIiIgogICAgbm9tYnJlID0gdmFsaWRhcl9ub192YWNpbyhub21icmUsICJub21icmUiKQogICAgZm9yIHBhaXMgaW4gcGFpc2VzOgogICAgICAgIGlmIHBhaXNbIm5vbWJyZSJdLmxvd2VyKCkgPT0gbm9tYnJlLmxvd2VyKCk6CiAgICAgICAgICAgIGlmIHBvYmxhY2lvbiBpcyBub3QgTm9uZToKICAgICAgICAgICAgICAgIHBhaXNbInBvYmxhY2lvbiJdID0gdmFsaWRhcl9lbnRlcm9fcG9zaXRpdm8ocG9ibGFjaW9uLCAicG9ibGFjaW9uIikKICAgICAgICAgICAgaWYgc3VwZXJmaWNpZSBpcyBub3QgTm9uZToKICAgICAgICAgICAgICAgIHBhaXNbInN1cGVyZmljaWUiXSA9IHZhbGlkYXJfZW50ZXJvX3Bvc2l0aXZvKHN1cGVyZmljaWUsICJzdXBlcmZpY2llIikKICAgICAgICAgICAgcmV0dXJuIFRydWUKICAgIHByaW50KGYiTm8gc2UgZW5jb250csOzIGVsIHBhw61zICd7bm9tYnJlfScuIikKICAgIHJldHVybiBGYWxzZQoKCiMgLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tCiMgQsO6c3F1ZWRhcyB5IGZpbHRyb3MKIyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0KCmRlZiBidXNjYXJfcGFpc19wb3Jfbm9tYnJlKHBhaXNlczogTGlzdFtEaWN0XSwgbm9tYnJlOiBzdHIsCiAgICAgICAgICAgICAgICAgICAgICAgICAgIGV4YWN0bzogYm9vbCA9IEZhbHNlKSAtPiBMaXN0W0RpY3RdOgogICAgIiIiQnVzY2EgcGHDrXNlcyBwb3Igbm9tYnJlIChpZ25vcmFuZG8gdGlsZGVzIHkgbWF5w7pzY3VsYXMpLgoKICAgIFNpIGV4YWN0bz1UcnVlLCBsYSBjb2luY2lkZW5jaWEgZXMgZXhhY3RhLgogICAgU2kgZXhhY3RvPUZhbHNlLCBzZSBidXNjYSBjb2luY2lkZW5jaWEgcGFyY2lhbCAoY29udGllbmUpLgogICAgIiIiCiAgICBub21icmVfbm9ybSA9IG5vcm1hbGl6YXJfdGV4dG8odmFsaWRhcl9ub192YWNpbyhub21icmUsICJub21icmUiKSkKICAgIHJlc3VsdGFkb3MgPSBbXQogICAgZm9yIHBhaXMgaW4gcGFpc2VzOgogICAgICAgIG5vbWJyZV9wYWlzX25vcm0gPSBub3JtYWxpemFyX3RleHRvKHBhaXNbIm5vbWJyZSJdKQogICAgICAgIGlmIGV4YWN0byBhbmQgbm9tYnJlX3BhaXNfbm9ybSA9PSBub21icmVfbm9ybToKICAgICAgICAgICAgcmVzdWx0YWRvcy5hcHBlbmQocGFpcykKICAgICAgICBlbGlmIChub3QgZXhhY3RvKSBhbmQgbm9tYnJlX25vcm0gaW4gbm9tYnJlX3BhaXNfbm9ybToKICAgICAgICAgICAgcmVzdWx0YWRvcy5hcHBlbmQocGFpcykKICAgIHJldHVybiByZXN1bHRhZG9zCgoKZGVmIGZpbHRyYXJfcG9yX2NvbnRpbmVudGUocGFpc2VzOiBMaXN0W0RpY3RdLCBjb250aW5lbnRlOiBzdHIpIC0+IExpc3RbRGljdF06CiAgICAiIiJGaWx0cmEgcGHDrXNlcyBwb3IgY29udGluZW50ZSAoaWdub3JhbmRvIHRpbGRlcyB5IG1hecO6c2N1bGFzKS4KCiAgICBMYSBjb2luY2lkZW5jaWEgZXMgcGFyY2lhbDogImFtZXJpYyIgZW5jdWVudHJhICJBbcOpcmljYSIuCiAgICAiIiIKICAgIGNvbnRpbmVudGVfbm9ybSA9IG5vcm1hbGl6YXJfdGV4dG8odmFsaWRhcl9ub192YWNpbyhjb250aW5lbnRlLCAiY29udGluZW50ZSIpKQogICAgcmV0dXJuIFtwIGZvciBwIGluIHBhaXNlcwogICAgICAgICAgICBpZiBjb250aW5lbnRlX25vcm0gaW4gbm9ybWFsaXphcl90ZXh0byhwWyJjb250aW5lbnRlIl0pXQoKCmRlZiBmaWx0cmFyX3Bvcl9yYW5nb19wb2JsYWNpb24ocGFpc2VzOiBMaXN0W0RpY3RdLCBtaW5pbW86IEFueSwgbWF4aW1vOiBBbnkpIC0+IExpc3RbRGljdF06CiAgICAiIiJGaWx0cmEgcGHDrXNlcyBjdXlhIHBvYmxhY2nDs24gZXN0w6kgZGVudHJvIGRlbCByYW5nbyBbbWluaW1vLCBtYXhpbW9dLiIiIgogICAgbWluX3AgPSB2YWxpZGFyX2VudGVyb19wb3NpdGl2byhtaW5pbW8sICJwb2JsYWNpb24gbcOtbmltYSIpCiAgICBtYXhfcCA9IHZhbGlkYXJfZW50ZXJvX3Bvc2l0aXZvKG1heGltbywgInBvYmxhY2lvbiBtw6F4aW1hIikKICAgIGlmIG1pbl9wID4gbWF4X3A6CiAgICAgICAgbWluX3AsIG1heF9wID0gbWF4X3AsIG1pbl9wCiAgICByZXR1cm4gW3AgZm9yIHAgaW4gcGFpc2VzIGlmIG1pbl9wIDw9IHBbInBvYmxhY2lvbiJdIDw9IG1heF9wXQoKCmRlZiBmaWx0cmFyX3Bvcl9yYW5nb19zdXBlcmZpY2llKHBhaXNlczogTGlzdFtEaWN0XSwgbWluaW1vOiBBbnksIG1heGltbzogQW55KSAtPiBMaXN0W0RpY3RdOgogICAgIiIiRmlsdHJhIHBhw61zZXMgY3V5YSBzdXBlcmZpY2llIGVzdMOpIGRlbnRybyBkZWwgcmFuZ28gW21pbmltbywgbWF4aW1vXS4iIiIKICAgIG1pbl9zID0gdmFsaWRhcl9lbnRlcm9fcG9zaXRpdm8obWluaW1vLCAic3VwZXJmaWNpZSBtw61uaW1hIikKICAgIG1heF9zID0gdmFsaWRhcl9lbnRlcm9fcG9zaXRpdm8obWF4aW1vLCAic3VwZXJmaWNpZSBtw6F4aW1hIikKICAgIGlmIG1pbl9zID4gbWF4X3M6CiAgICAgICAgbWluX3MsIG1heF9zID0gbWF4X3MsIG1pbl9zCiAgICByZXR1cm4gW3AgZm9yIHAgaW4gcGFpc2VzIGlmIG1pbl9zIDw9IHBbInN1cGVyZmljaWUiXSA8PSBtYXhfc10KCgojIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQojIE9yZGVuYW1pZW50b3MKIyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0KCkNMQVZFU19PUkRFTl9WQUxJREFTID0gKCJub21icmUiLCAicG9ibGFjaW9uIiwgInN1cGVyZmljaWUiLCAiY29udGluZW50ZSIpCgoKZGVmIG9yZGVuYXJfcGFpc2VzKHBhaXNlczogTGlzdFtEaWN0XSwgY2xhdmU6IHN0ciA9ICJub21icmUiLAogICAgICAgICAgICAgICAgICAgZGVzY2VuZGVudGU6IGJvb2wgPSBGYWxzZSkgLT4gTGlzdFtEaWN0XToKICAgICIiIkRldnVlbHZlIHVuYSBudWV2YSBsaXN0YSBkZSBwYcOtc2VzIG9yZGVuYWRhIHBvciBsYSBjbGF2ZSBpbmRpY2FkYS4KCiAgICBMYSBsaXN0YSBvcmlnaW5hbCBubyBzZSBtb2RpZmljYS4gQ2xhdmVzIHbDoWxpZGFzOiBub21icmUsIHBvYmxhY2lvbiwKICAgIHN1cGVyZmljaWUsIGNvbnRpbmVudGUuCiAgICAiIiIKICAgIGNsYXZlID0gY2xhdmUuc3RyaXAoKS5sb3dlcigpCiAgICBpZiBjbGF2ZSBub3QgaW4gQ0xBVkVTX09SREVOX1ZBTElEQVM6CiAgICAgICAgcmFpc2UgVmFsdWVFcnJvcihmIkNsYXZlIGRlIG9yZGVuYW1pZW50byBpbnbDoWxpZGE6ICd7Y2xhdmV9Jy4gIgogICAgICAgICAgICAgICAgICAgICAgICAgZiJPcGNpb25lczogeycsICcuam9pbihDTEFWRVNfT1JERU5fVkFMSURBUyl9LiIpCiAgICAjIENvcGlhIHBhcmEgbm8gbXV0YXIgbGEgbGlzdGEgb3JpZ2luYWwKICAgIGNvcGlhID0gbGlzdChwYWlzZXMpCgogICAgZGVmIGNsYXZlX29yZGVuKHBhaXMpOgogICAgICAgIHZhbG9yID0gcGFpc1tjbGF2ZV0KICAgICAgICAjIFNpIGVzIHRleHRvLCBvcmRlbmFyIHNpbiBkaXN0aW5ndWlyIG1hecO6c2N1bGFzL21pbsO6c2N1bGFzCiAgICAgICAgaWYgaXNpbnN0YW5jZSh2YWxvciwgc3RyKToKICAgICAgICAgICAgcmV0dXJuIHZhbG9yLmxvd2VyKCkKICAgICAgICByZXR1cm4gdmFsb3IKCiAgICBjb3BpYS5zb3J0KGtleT1jbGF2ZV9vcmRlbiwgcmV2ZXJzZT1kZXNjZW5kZW50ZSkKICAgIHJldHVybiBjb3BpYQoKCiMgLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tCiMgRXN0YWTDrXN0aWNhcwojIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQoKZGVmIHBhaXNfbWF5b3JfcG9ibGFjaW9uKHBhaXNlczogTGlzdFtEaWN0XSkgLT4gT3B0aW9uYWxbRGljdF06CiAgICAiIiJEZXZ1ZWx2ZSBlbCBwYcOtcyBjb24gbWF5b3IgcG9ibGFjacOzbiwgbyBOb25lIHNpIGxhIGxpc3RhIGVzdMOhIHZhY8OtYS4iIiIKICAgIGlmIG5vdCBwYWlzZXM6CiAgICAgICAgcmV0dXJuIE5vbmUKICAgIHJldHVybiBtYXgocGFpc2VzLCBrZXk9bGFtYmRhIHA6IHBbInBvYmxhY2lvbiJdKQoKCmRlZiBwYWlzX21lbm9yX3BvYmxhY2lvbihwYWlzZXM6IExpc3RbRGljdF0pIC0+IE9wdGlvbmFsW0RpY3RdOgogICAgIiIiRGV2dWVsdmUgZWwgcGHDrXMgY29uIG1lbm9yIHBvYmxhY2nDs24sIG8gTm9uZSBzaSBsYSBsaXN0YSBlc3TDoSB2YWPDrWEuIiIiCiAgICBpZiBub3QgcGFpc2VzOgogICAgICAgIHJldHVybiBOb25lCiAgICByZXR1cm4gbWluKHBhaXNlcywga2V5PWxhbWJkYSBwOiBwWyJwb2JsYWNpb24iXSkKCgpkZWYgcHJvbWVkaW9fcG9ibGFjaW9uKHBhaXNlczogTGlzdFtEaWN0XSkgLT4gZmxvYXQ6CiAgICAiIiJDYWxjdWxhIGVsIHByb21lZGlvIGRlIHBvYmxhY2nDs24uIERldnVlbHZlIDAuMCBzaSBsYSBsaXN0YSBlc3TDoSB2YWPDrWEuIiIiCiAgICBpZiBub3QgcGFpc2VzOgogICAgICAgIHJldHVybiAwLjAKICAgIHJldHVybiBzdW0ocFsicG9ibGFjaW9uIl0gZm9yIHAgaW4gcGFpc2VzKSAvIGxlbihwYWlzZXMpCgoKZGVmIHByb21lZGlvX3N1cGVyZmljaWUocGFpc2VzOiBMaXN0W0RpY3RdKSAtPiBmbG9hdDoKICAgICIiIkNhbGN1bGEgZWwgcHJvbWVkaW8gZGUgc3VwZXJmaWNpZS4gRGV2dWVsdmUgMC4wIHNpIGxhIGxpc3RhIGVzdMOhIHZhY8OtYS4iIiIKICAgIGlmIG5vdCBwYWlzZXM6CiAgICAgICAgcmV0dXJuIDAuMAogICAgcmV0dXJuIHN1bShwWyJzdXBlcmZpY2llIl0gZm9yIHAgaW4gcGFpc2VzKSAvIGxlbihwYWlzZXMpCgoKZGVmIGNhbnRpZGFkX3Bvcl9jb250aW5lbnRlKHBhaXNlczogTGlzdFtEaWN0XSkgLT4gRGljdFtzdHIsIGludF06CiAgICAiIiJEZXZ1ZWx2ZSB1biBkaWNjaW9uYXJpbyB7Y29udGluZW50ZTogY2FudGlkYWQgZGUgcGHDrXNlc30uIiIiCiAgICByZXN1bHRhZG86IERpY3Rbc3RyLCBpbnRdID0ge30KICAgIGZvciBwYWlzIGluIHBhaXNlczoKICAgICAgICBjb250ID0gcGFpc1siY29udGluZW50ZSJdCiAgICAgICAgcmVzdWx0YWRvW2NvbnRdID0gcmVzdWx0YWRvLmdldChjb250LCAwKSArIDEKICAgIHJldHVybiByZXN1bHRhZG8KCgojIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQojIFByZXNlbnRhY2nDs24KIyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0KCmRlZiBmb3JtYXRlYXJfbnVtZXJvKG51bWVybzogaW50KSAtPiBzdHI6CiAgICAiIiJGb3JtYXRlYSB1biBuw7ptZXJvIGNvbiBzZXBhcmFkb3IgZGUgbWlsZXMuIiIiCiAgICByZXR1cm4gZiJ7bnVtZXJvOix9Ii5yZXBsYWNlKCIsIiwgIi4iKQoKCmRlZiBtb3N0cmFyX3BhaXMocGFpczogRGljdCkgLT4gTm9uZToKICAgICIiIkltcHJpbWUgbG9zIGRhdG9zIGRlIHVuIHBhw61zIGRlIGZvcm1hIGxlZ2libGUuIiIiCiAgICBwcmludChmIiAgLSB7cGFpc1snbm9tYnJlJ119OiBwb2JsYWNpw7NuPXtmb3JtYXRlYXJfbnVtZXJvKHBhaXNbJ3BvYmxhY2lvbiddKX0sICIKICAgICAgICAgIGYic3VwZXJmaWNpZT17Zm9ybWF0ZWFyX251bWVybyhwYWlzWydzdXBlcmZpY2llJ10pfSBrbcKyLCAiCiAgICAgICAgICBmImNvbnRpbmVudGU9e3BhaXNbJ2NvbnRpbmVudGUnXX0iKQoKCmRlZiBtb3N0cmFyX2xpc3RhKHBhaXNlczogTGlzdFtEaWN0XSwgdGl0dWxvOiBzdHIgPSAiUGHDrXNlcyIpIC0+IE5vbmU6CiAgICAiIiJJbXByaW1lIHVuYSBsaXN0YSBkZSBwYcOtc2VzIGNvbiB1biB0w610dWxvLiIiIgogICAgcHJpbnQoZiJcbi0tLSB7dGl0dWxvfSAoe2xlbihwYWlzZXMpfSkgLS0tIikKICAgIGlmIG5vdCBwYWlzZXM6CiAgICAgICAgcHJpbnQoIiAgKHNpbiByZXN1bHRhZG9zKSIpCiAgICAgICAgcmV0dXJuCiAgICBmb3IgcGFpcyBpbiBwYWlzZXM6CiAgICAgICAgbW9zdHJhcl9wYWlzKHBhaXMpCiAgICBwcmludCgpCg==").decode("utf-8")
    _paises_mod = type("paises", (), {})()
    exec(compile(_paises_code, "paises.py", "exec"), _paises_mod.__dict__)
for _name in dir(_paises_mod):
    if not _name.startswith("_"):
        globals()[_name] = getattr(_paises_mod, _name)

RUTA_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "paises.csv")


def leer_texto(mensaje: str) -> str:
    """Lee un texto no vacío desde consola, validando la entrada."""
    while True:
        try:
            valor = input(mensaje)
        except (EOFError, KeyboardInterrupt):
            print("\nOperación cancelada.")
            return ""
        try:
            return validar_no_vacio(valor, "entrada")
        except ValueError as e:
            print(f"  Error: {e}")


def leer_entero(mensaje: str) -> int:
    """Lee un entero positivo desde consola, validando la entrada."""
    while True:
        try:
            valor = input(mensaje)
        except (EOFError, KeyboardInterrupt):
            print("\nOperación cancelada.")
            return 0
        try:
            return validar_entero_positivo(valor, "entrada")
        except ValueError as e:
            print(f"  Error: {e}")


def opcion_agregar(paises: list) -> None:
    print("\n--- Agregar país ---")
    nombre = leer_texto("Nombre del país: ")
    if not nombre:
        return
    try:
        poblacion = leer_entero("Población (entero positivo): ")
        if poblacion == 0:
            return
        superficie = leer_entero("Superficie en km² (entero positivo): ")
        if superficie == 0:
            return
        continente = leer_texto("Continente: ")
        if not continente:
            return
        pais = crear_pais(nombre, poblacion, superficie, continente)
    except ValueError as e:
        print(f"  Error al crear el país: {e}")
        return

    if agregar_pais(paises, pais):
        print(f"  País '{pais['nombre']}' agregado correctamente.")
        if guardar_paises(RUTA_CSV, paises):
            print("  Cambios guardados en el CSV.")
    else:
        print("  No se agregó el país.")


def opcion_actualizar(paises: list) -> None:
    print("\n--- Actualizar país ---")
    nombre = leer_texto("Nombre del país a actualizar: ")
    if not nombre:
        return
    resultados = buscar_pais_por_nombre(paises, nombre, exacto=True)
    if not resultados:
        # Intentar búsqueda parcial
        resultados = buscar_pais_por_nombre(paises, nombre, exacto=False)
        if not resultados:
            print(f"  No se encontró ningún país con el nombre '{nombre}'.")
            return
        if len(resultados) > 1:
            print("  Se encontraron varios países:")
            for p in resultados:
                print(f"    - {p['nombre']}")
            nombre = leer_texto("Indique el nombre exacto del país: ")
            if not nombre:
                return
            resultados = buscar_pais_por_nombre(paises, nombre, exacto=True)
            if not resultados:
                print("  No se encontró el país indicado.")
                return

    pais = resultados[0]
    print(f"  País seleccionado: {pais['nombre']} "
          f"(población={pais['poblacion']}, superficie={pais['superficie']})")

    actualizar_poblacion = leer_texto("¿Actualizar población? (s/n): ").lower()
    nueva_poblacion = None
    if actualizar_poblacion == "s":
        nueva_poblacion = leer_entero("Nueva población: ")
        if nueva_poblacion == 0:
            nueva_poblacion = None

    actualizar_superficie = leer_texto("¿Actualizar superficie? (s/n): ").lower()
    nueva_superficie = None
    if actualizar_superficie == "s":
        nueva_superficie = leer_entero("Nueva superficie en km²: ")
        if nueva_superficie == 0:
            nueva_superficie = None

    if nueva_poblacion is None and nueva_superficie is None:
        print("  No se realizaron cambios.")
        return

    try:
        if actualizar_pais(paises, pais["nombre"], nueva_poblacion, nueva_superficie):
            print("  País actualizado correctamente.")
            if guardar_paises(RUTA_CSV, paises):
                print("  Cambios guardados en el CSV.")
    except ValueError as e:
        print(f"  Error al actualizar: {e}")


def opcion_buscar(paises: list) -> None:
    print("\n--- Buscar país ---")
    nombre = leer_texto("Nombre (o parte del nombre) del país: ")
    if not nombre:
        return
    tipo = leer_texto("¿Coincidencia exacta? (s/n): ").lower()
    exacto = (tipo == "s")
    resultados = buscar_pais_por_nombre(paises, nombre, exacto=exacto)
    if resultados:
        mostrar_lista(resultados, "Resultados de búsqueda")
    else:
        print(f"  No se encontraron países que coincidan con '{nombre}'.")


def opcion_filtrar(paises: list) -> None:
    print("\n--- Filtrar países ---")
    print("  1. Por continente")
    print("  2. Por rango de población")
    print("  3. Por rango de superficie")
    opcion = leer_texto("Seleccione una opción: ")
    if opcion == "1":
        continente = leer_texto("Continente: ")
        if not continente:
            return
        try:
            resultados = filtrar_por_continente(paises, continente)
        except ValueError as e:
            print(f"  Error: {e}")
            return
        mostrar_lista(resultados, f"Países en {continente}")
    elif opcion == "2":
        minimo = leer_entero("Población mínima: ")
        if minimo == 0:
            return
        maximo = leer_entero("Población máxima: ")
        if maximo == 0:
            return
        try:
            resultados = filtrar_por_rango_poblacion(paises, minimo, maximo)
        except ValueError as e:
            print(f"  Error: {e}")
            return
        mostrar_lista(resultados, f"Países con población entre {minimo} y {maximo}")
    elif opcion == "3":
        minimo = leer_entero("Superficie mínima (km²): ")
        if minimo == 0:
            return
        maximo = leer_entero("Superficie máxima (km²): ")
        if maximo == 0:
            return
        try:
            resultados = filtrar_por_rango_superficie(paises, minimo, maximo)
        except ValueError as e:
            print(f"  Error: {e}")
            return
        mostrar_lista(resultados, f"Países con superficie entre {minimo} y {maximo} km²")
    else:
        print("  Opción inválida.")


def opcion_ordenar(paises: list) -> None:
    print("\n--- Ordenar países ---")
    print("  Claves disponibles: nombre, poblacion, superficie, continente")
    clave = leer_texto("Ordenar por: ")
    if not clave:
        return
    orden = leer_texto("¿Descendente? (s/n): ").lower()
    descendente = (orden == "s")
    try:
        resultados = ordenar_paises(paises, clave, descendente=descendente)
    except ValueError as e:
        print(f"  Error: {e}")
        return
    direccion = "descendente" if descendente else "ascendente"
    mostrar_lista(resultados, f"Países ordenados por {clave} ({direccion})")


def opcion_estadisticas(paises: list) -> None:
    print("\n--- Estadísticas ---")
    if not paises:
        print("  No hay países cargados.")
        return

    mayor = pais_mayor_poblacion(paises)
    menor = pais_menor_poblacion(paises)
    prom_pob = promedio_poblacion(paises)
    prom_sup = promedio_superficie(paises)
    por_continente = cantidad_por_continente(paises)

    print(f"  País con mayor población: {mayor['nombre']} "
          f"({mayor['poblacion']:,} habitantes)".replace(",", "."))
    print(f"  País con menor población: {menor['nombre']} "
          f"({menor['poblacion']:,} habitantes)".replace(",", "."))
    print(f"  Promedio de población: {prom_pob:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    print(f"  Promedio de superficie: {prom_sup:,.2f} km²".replace(",", "X").replace(".", ",").replace("X", "."))
    print("  Cantidad de países por continente:")
    for continente, cantidad in sorted(por_continente.items()):
        print(f"    - {continente}: {cantidad}")


def mostrar_menu() -> None:
    print("\n" + "=" * 50)
    print("  GESTIÓN DE PAÍSES - MENÚ PRINCIPAL")
    print("=" * 50)
    print("  1. Agregar país")
    print("  2. Actualizar país (población/superficie)")
    print("  3. Buscar país por nombre")
    print("  4. Filtrar países")
    print("  5. Ordenar países")
    print("  6. Mostrar estadísticas")
    print("  7. Listar todos los países")
    print("  8. Guardar y salir")
    print("=" * 50)


def main() -> None:
    print("Cargando dataset de países...")
    paises = cargar_paises(RUTA_CSV)
    print(f"Se cargaron {len(paises)} países desde '{RUTA_CSV}'.")

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            opcion_agregar(paises)
        elif opcion == "2":
            opcion_actualizar(paises)
        elif opcion == "3":
            opcion_buscar(paises)
        elif opcion == "4":
            opcion_filtrar(paises)
        elif opcion == "5":
            opcion_ordenar(paises)
        elif opcion == "6":
            opcion_estadisticas(paises)
        elif opcion == "7":
            mostrar_lista(paises, "Todos los países")
        elif opcion == "8":
            if guardar_paises(RUTA_CSV, paises):
                print("Datos guardados. ¡Hasta luego!")
            else:
                print("No se pudieron guardar los datos.")
            break
        else:
            print("Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    main()
