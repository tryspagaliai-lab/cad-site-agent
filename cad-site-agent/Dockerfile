# CAD Site Agent — pilnai izoliuotas konteineris (alternatyva native diegimui).
#
# Build (VPS'e, projekto šaknyje):
#     docker build -t cad-agent .
#
# Naudojimas — sumontuok darbinį katalogą su DXF failais į /work:
#     docker run --rm -v "$PWD/work:/work" cad-agent process /work/input.dxf /work/output/result.dxf
#
FROM python:3.11-slim AS base

# Sistemos bibliotekos (shapely/scipy wheel'ai self-contained; libgeos kaip atsarga)
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential \
      libgeos-dev \
      libspatialindex-dev \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Pirma tik metaduomenys — geresnis Docker sluoksnių kešavimas
COPY pyproject.toml README.md ./
COPY src ./src
COPY config ./config

RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir .

# Darbinis katalogas DXF įvestims/išvestims (montuojamas per -v)
WORKDIR /work

ENTRYPOINT ["cad-agent"]
CMD ["--help"]
