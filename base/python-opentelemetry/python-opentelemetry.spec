
# See eachdist.ini:
%global stable_version 1.10.0
%global prerel_version 0.29~b0
# Contents of python3-opentelemetry-proto are generated from proto files in a
# separate repository with a separate version number. We treat these as
# generated sources: we aren’t required by the guidelines to re-generate them
# (although we *may*) but we must include the original sources.
#
# See PROTO_REPO_BRANCH_OR_COMMIT in scripts/proto_codegen.sh for the correct
# version number.
%global proto_version 0.12.0

# Unfortunately, we cannot disable the prerelease packages without breaking
# almost all of the stable packages, because opentelemetry-sdk depends on the
# prerelease package opentelementry-semantic-conventions.
%bcond_without prerelease
# There are also experimental packages in eachdist.ini, with yet another
# version, but currently none of these actually exist. We will avoid packaging
# them if at all possible.

# Sphinx-generated HTML documentation is not suitable for packaging; see
# https://bugzilla.redhat.com/show_bug.cgi?id=2006555 for discussion.
#
# We can generate PDF documentation as a substitute.
%bcond_without doc_pdf

Name:           python-opentelemetry
Version:        %{stable_version}
%forgemeta
Release:        %autorelease
Summary:        OpenTelemetry Python API and SDK

License:        ASL 2.0
URL:            https://github.com/open-telemetry/opentelemetry-python
Source0:        %{url}/archive/v%{version}/opentelemetry-python-%{version}.tar.gz
# Note that we do not currently use this source, but it contains the original
# .proto files for python3-opentelemetry-proto, so we must include it.
%global proto_url https://github.com/open-telemetry/opentelemetry-proto
Source1:        %{proto_url}/archive/v%{proto_version}/opentelemetry-proto-%{proto_version}.tar.gz

# Wrong installation path in exporter “convenience” packages
# https://github.com/open-telemetry/opentelemetry-python/issues/2020
#
# Fix exporter-{jaeger,otlp,zipkin} install paths
# https://github.com/open-telemetry/opentelemetry-python/pull/2525
Patch0:         %{url}/pull/2525.patch

# Fix a mixed-up changelog entry
# https://github.com/open-telemetry/opentelemetry-python/pull/2526
Patch1:         %{url}/pull/2526.patch

BuildRequires:  python3-devel
# opentelemetry-exporter-opencensus install_requires: setuptools >= 16.0
# opentelemetry-api install_requires: setuptools >= 16.0
# opentelemetry-sdk install_requires: setuptools >= 16.0
BuildRequires:  %{py3_dist setuptools} >= 16.0

# Documentation
%if %{with doc_pdf}
BuildRequires:  make
BuildRequires:  python3-sphinx-latex
BuildRequires:  latexmk
%endif

# opentelemetry-proto install_requires: aiocontextvars; python_version<'3.7'

# opentelemetry-exporter-otlp-proto-grpc install_requires: backoff ~= 1.10.0
# opentelemetry-exporter-otlp-proto-http install_requires: backoff ~= 1.10.0
BuildRequires:  ((%{py3_dist backoff} >= 1.10) with (%{py3_dist backoff} < 1.11.0))

# dev-requirements.txt: black~=20.8b1
# (formatters/linters/typecheckers/coverage omitted)

# docs-requirements.txt: # Required by instrumentation and exporter packages
# docs-requirements.txt: ddtrace>=0.34.0
# (mentioned in a README but does not seem to actually be used anywhere)

# docs-requirements.txt: # Required by instrumentation and exporter packages
# docs-requirements.txt: Deprecated>=1.2.6
# opentelemetry-proto install_requires: Deprecated >= 1.2.6
# opentelemetry-propagator-b3 install_requires: deprecated >= 1.2.6
# opentelemetry-opentracing-shim install_requires: Deprecated >= 1.2.6
BuildRequires:  %{py3_dist Deprecated} >= 1.2.6

# docs-requirements.txt: # Required by instrumentation and exporter packages
# docs-requirements.txt: django>=2.2
BuildRequires:  %{py3_dist django} >= 2.2

# dev-requirements.txt: flake8~=3.7
# (formatters/linters/typecheckers/coverage omitted)

# tox.ini testenv.deps: opentelemetry: flaky
BuildRequires:  %{py3_dist flaky}

# docs-requirements.txt: # Required by instrumentation and exporter packages
# docs-requirements.txt: flask~=1.0
# opentelemetry-test-utils extras_require[test]: flask~=1.0
# NOTE: We must loosen this to allow flask~=2.0.
BuildRequires:  ((%{py3_dist flask} >= 1.0) with (%{py3_dist flask} < 3.0))

# opentelemetry-exporter-jaeger-proto-grpc install_requires:
#   googleapis-common-protos ~= 1.52
# opentelemetry-exporter-otlp-proto-grpc install_requires:
#   googleapis-common-protos ~= 1.52
# opentelemetry-exporter-otlp-proto-http install_requires:
#   googleapis-common-protos ~= 1.52
BuildRequires:  ((%{py3_dist googleapis-common-protos} >= 1.52) with (%{py3_dist googleapis-common-protos} < 2.0))

# docs-requirements.txt: # Required by instrumentation and exporter packages
# docs-requirements.txt: grpcio~=1.27
# opentelemetry-exporter-jaeger-proto-grpc install_requires:
#   grpcio >= 1.0.0, < 2.0.0
# opentelemetry-exporter-opencensus install_requires: grpcio >= 1.0.0, < 2.0.0
# opentelemetry-exporter-otlp-proto-grpc install_requires:
#   grpcio >= 1.0.0, < 2.0.0
BuildRequires:  ((%{py3_dist grpcio} >= 1.27) with (%{py3_dist grpcio} < 2.0))

# dev-requirements.txt: grpcio-tools~=1.41.0
# (needed only if we run scripts/proto_codegen.sh)

# dev-requirements.txt: httpretty~=1.0
# (does not seem to actually be used anywhere)

# dev-requirements.txt: isort~=5.8
# (formatters/linters/typecheckers/coverage omitted)

# dev-requirements.txt: mypy-protobuf~=3.0.0
# (formatters/linters/typecheckers/coverage omitted)

# dev-requirements.txt: mypy==0.812
# (formatters/linters/typecheckers/coverage omitted)

# opentelemetry-exporter-opencensus install_requires:
#   opencensus-proto >= 0.1.0, < 1.0.0
BuildRequires:  ((%{py3_dist opencensus-proto} >= 0.1.0) with (%{py3_dist opencensus-proto} < 1.0.0))

# docs-requirements.txt: # Required by instrumentation and exporter packages
# docs-requirements.txt: opentracing~=2.2.0
# opentelemetry-opentracing-shim install_requires: opentracing ~= 2.0
# opentelemetry-opentracing-shim extras_require[test]: opentracing ~= 2.2.0
# NOTE: We must loosen this to allow opentracing 2.3.0 and 2.4.0.
BuildRequires:  ((%{py3_dist opentracing} >= 2.2.0) with (%{py3_dist opentracing} < 2.5.0))

# opentelemetry-exporter-prometheus install_requires:
#   prometheus_client >= 0.5.0, < 1.0.0
BuildRequires:  ((%{py3_dist prometheus_client} >= 0.5.0) with (%{py3_dist prometheus_client} < 1.0.0))

# dev-requirements.txt: protobuf>=3.18.1
# (possibly needed only if we run scripts/proto_codegen.sh?)
# opentelemetry-proto install_requires: protobuf>=3.13.0
# opentelemetry-exporter-opencensus install_requires: protobuf >= 3.13.0
# opentelemetry-exporter-zipkin-proto-http install_requires: protobuf >= 3.12
BuildRequires:  %{py3_dist protobuf} >= 3.18.1

# dev-requirements.txt: pylint==2.7.1
# (formatters/linters/typecheckers/coverage omitted)

# dev-requirements.txt: pytest-cov>=2.8
# (formatters/linters/typecheckers/coverage omitted)

# dev-requirements.txt: pytest>=6.0
# tox.ini testenv.deps: test: pytest
BuildRequires:  %{py3_dist pytest} >= 6.0

# tox.ini testenv.deps: test: pytest-benchmark
BuildRequires:  %{py3_dist pytest-benchmark}

# opentelemetry-exporter-otlp-proto-grpc extras_require[test]: pytest-grpc
BuildRequires:  %{py3_dist pytest-grpc}

# dev-requirements.txt: readme-renderer~=24.0
# (does not seem to actually be used anywhere)

# opentelemetry-exporter-zipkin-json install_requires: requests ~= 2.7
# opentelemetry-exporter-zipkin-proto-http install_requires: requests ~= 2.7
# opentelemetry-exporter-otlp-proto-http install_requires: requests ~= 2.7
BuildRequires:  ((%{py3_dist requests} >= 2.7) with (%{py3_dist requests} < 3.0))

# dev-requirements.txt: sphinx-autodoc-typehints~=1.12.0
# docs-requirements.txt: sphinx-autodoc-typehints~=1.12.0
# NOTE: We must loosen this to allow sphinx-autodoc-typehints~=1.12.
BuildRequires:  ((%{py3_dist sphinx-autodoc-typehints} >= 1.12.0) with (%{py3_dist sphinx-autodoc-typehints} < 2.0))

# dev-requirements.txt: sphinx-rtd-theme~=0.5
# docs-requirements.txt: sphinx-rtd-theme~=0.5
# NOTE: We must loosen this to allow sphinx-rtd-theme~=1.0.
# HOWEVER: we do not build the HTML documentation, so we can do without.

# dev-requirements.txt: sphinx~=3.5.4
# docs-requirements.txt: sphinx~=3.5.4
# NOTE: We must loosen this to allow Sphinx 3.6+ and 4.x.
BuildRequires:  ((%{py3_dist sphinx} >= 3.5.4) with (%{py3_dist sphinx} < 5.0))

# docs-requirements.txt: # used to generate docs for the website
# docs-requirements.txt: sphinx-jekyll-builder
# (omitted; we will not build website docs)

# docs-requirements.txt: # Required by instrumentation and exporter packages
# docs-requirements.txt: thrift>=0.10.0
# opentelemetry-exporter-jaeger-thrift install_requires: thrift >= 0.10.0
BuildRequires:  %{py3_dist thrift} >= 0.10.0

# opentelemetry-sdk install_requires: typing-extensions >= 3.7.4
BuildRequires:  %{py3_dist typing-extensions} >= 3.7.4

# docs-requirements.txt: # Required by instrumentation and exporter packages
# docs-requirements.txt: wrapt>=1.0.0,<2.0.0
# Now that instrumentation is moved to contrib, this is no longer used
# directly. (It is a dependency for some examples, and is in the intersphinx
# mapping, which we don’t use since the build is offline, for the docs.)
# BuildRequires:  ((%%{py3_dist wrapt} >= 1.0.0) with (%%{py3_dist wrapt} < 2.0.0))

# docs-requirements.txt: # Need to install the api/sdk in the venv for
#   autodoc. Modifying sys.path
# docs-requirements.txt: # doesn't work for pkg_resources.
# docs-requirements.txt: ./opentelemetry-api
# opentelemetry-sdk install_requires: opentelemetry-api == %%{stable_version}
# opentelemetry-propagator-b3 install_requires: opentelemetry-api ~= 1.3
# opentelemetry-propagator-jaeger install_requires: opentelemetry-api ~= 1.3
# opentelemetry-exporter-jaeger-proto-grpc install_requires:
#   opentelemetry-api ~= 1.3
# opentelemetry-exporter-jaeger-thrift install_requires:
#   opentelemetry-api ~= 1.3
# opentelemetry-exporter-opencensus install_requires: opentelemetry-api ~= 1.3
# opentelemetry-exporter-otlp-proto-grpc install_requires:
#   opentelemetry-api ~= 1.3
# opentelemetry-exporter-otlp-proto-http install_requires:
#   opentelemetry-api ~= 1.3
# opentelemetry-exporter-prometheus install_requires:
#   opentelemetry-api >= 1.10.0
# opentelemetry-exporter-zipkin-json install_requires:
#   opentelemetry-api ~= 1.3
# opentelemetry-exporter-zipkin-proto-http install_requires:
#   opentelemetry-api ~= 1.3
# opentelemetry-opentracing-shim install_requires: opentelemetry-api ~= 1.3
# opentelemetry-test-utils install_requires: opentelemetry-api ~= 1.3

# opentelemetry-exporter-otlp-proto-grpc install_requires:
#   opentelemetry-proto == %%{stable_version}
# opentelemetry-exporter-otlp-proto-http install_requires:
#   opentelemetry-proto == %%{stable_version}

# docs-requirements.txt: # Need to install the api/sdk in the venv for
#   autodoc. Modifying sys.path
# docs-requirements.txt: # doesn't work for pkg_resources.
# docs-requirements.txt: ./opentelemetry-sdk
# opentelemetry-exporter-jaeger-proto-grpc install_requires:
#   opentelemetry-sdk ~= 1.3
# opentelemetry-exporter-opencensus install_requires: opentelemetry-sdk ~= 1.3
# opentelemetry-exporter-otlp-proto-grpc install_requires:
#   opentelemetry-sdk ~= 1.10.0
# opentelemetry-exporter-otlp-proto-http install_requires:
#   opentelemetry-sdk ~= 1.3
# opentelemetry-exporter-prometheus install_requires:
#   opentelemetry-sdk >= 1.10.0
# opentelemetry-exporter-zipkin-json install_requires:
#   opentelemetry-sdk ~= 1.3
# opentelemetry-exporter-jaeger-thrift install_requires:
#   opentelemetry-sdk ~= 1.3
# opentelemetry-exporter-zipkin-proto-http install_requires:
#   opentelemetry-sdk ~= 1.3
# opentelemetry-test-utils install_requires: opentelemetry-sdk ~= 1.3

# docs-requirements.txt: # Need to install the api/sdk in the venv for
#   autodoc. Modifying sys.path
# docs-requirements.txt: # doesn't work for pkg_resources.
# docs-requirements.txt: ./opentelemetry-semantic-conventions
# opentelemetry-sdk install_requires:
#   opentelemetry-semantic-conventions == %%{prerel_version}

# opentelemetry-exporter-jaeger install_requires:
#   opentelemetry-exporter-jaeger-proto-grpc == %%{stable_version}

# opentelemetry-exporter-jaeger install_requires:
#   opentelemetry-exporter-jaeger-thrift == %%{stable_version}

# opentelemetry-exporter-otlp install_requires:
#   opentelemetry-exporter-otlp-proto-grpc == %%{stable_version}

# opentelemetry-exporter-otlp install_requires:
#   opentelemetry-exporter-otlp-proto-http == %%{stable_version}

# opentelemetry-exporter-zipkin-proto-http install_requires:
#   opentelemetry-exporter-zipkin-json == %%{stable_version}
# opentelemetry-exporter-zipkin install_requires:
#   opentelemetry-exporter-zipkin-json == %%{stable_version}

# opentelemetry-exporter-zipkin install_requires:
#   opentelemetry-exporter-zipkin-proto-http == %%{stable_version}

# opentelemetry-opentracing-shim extras_require[test]:
#   opentelemetry-test-utils == %%{prerel_version}

BuildArch:      noarch

%global stable_eggversion %(echo '%{stable_version}' | tr -d '~^')
%global stable_egginfo %{stable_eggversion}-py%{python3_version}.egg-info
%global prerel_eggversion %(echo '%{prerel_version}' | tr -d '~^')
%global prerel_egginfo %{prerel_eggversion}-py%{python3_version}.egg-info

%global common_description %{expand:
OpenTelemetry Python API and SDK.}

%description
%{common_description}


%package -n python3-opentelemetry-exporter-jaeger-proto-grpc
Summary:        Jaeger Protobuf Exporter for OpenTelemetry
Version:        %{stable_version}

# Dependencies across subpackages should be fully-versioned. See comments
# following BuildRequires for a tabulation of such interdependencies.
Requires:       python3-opentelemetry-api = %{stable_version}-%{release}
Requires:       python3-opentelemetry-sdk = %{stable_version}-%{release}

%description -n python3-opentelemetry-exporter-jaeger-proto-grpc
This library allows to export tracing data to Jaeger
(https://www.jaegertracing.io/).


%package -n python3-opentelemetry-exporter-jaeger-thrift
Summary:        Jaeger Thrift Exporter for OpenTelemetry
Version:        %{stable_version}

# Dependencies across subpackages should be fully-versioned. See comments
# following BuildRequires for a tabulation of such interdependencies.
Requires:       python3-opentelemetry-api = %{stable_version}-%{release}
Requires:       python3-opentelemetry-sdk = %{stable_version}-%{release}

%description -n python3-opentelemetry-exporter-jaeger-thrift
This library allows to export tracing data to Jaeger
(https://www.jaegertracing.io/) using Thrift.


%package -n python3-opentelemetry-exporter-jaeger
Summary:        Jaeger Exporters for OpenTelemetry
Version:        %{stable_version}

Obsoletes:      python3-opentelemetry-ext-jaeger < 1.0

# Dependencies across subpackages should be fully-versioned. See comments
# following BuildRequires for a tabulation of such interdependencies.
Requires:       python3-opentelemetry-exporter-jaeger-proto-grpc = %{stable_version}-%{release}
Requires:       python3-opentelemetry-exporter-jaeger-thrift = %{stable_version}-%{release}

%description -n python3-opentelemetry-exporter-jaeger
This library is provided as a convenience to install all supported Jaeger
Exporters. Currently it installs:
  • opentelemetry-exporter-jaeger-proto-grpc
  • opentelemetry-exporter-jaeger-thrift

To avoid unnecessary dependencies, users should install the specific package
once they’ve determined their preferred serialization method.


%if %{with prerelease}
%package -n python3-opentelemetry-exporter-opencensus
Summary:        OpenCensus Exporter
Version:        %{prerel_version}

Obsoletes:      python3-opentelemetry-ext-opencensusexporter < 1.0

# Dependencies across subpackages should be fully-versioned. See comments
# following BuildRequires for a tabulation of such interdependencies.
Requires:       python3-opentelemetry-api = %{stable_version}-%{release}
Requires:       python3-opentelemetry-sdk = %{stable_version}-%{release}

%description -n python3-opentelemetry-exporter-opencensus
This library allows to export traces using OpenCensus.
%endif


%package -n python3-opentelemetry-exporter-otlp-proto-grpc
Summary:        OpenTelemetry Collector Protobuf over gRPC Exporter
Version:        %{stable_version}

# Dependencies across subpackages should be fully-versioned. See comments
# following BuildRequires for a tabulation of such interdependencies.
Requires:       python3-opentelemetry-api = %{stable_version}-%{release}
Requires:       python3-opentelemetry-sdk = %{stable_version}-%{release}
Requires:       python3-opentelemetry-proto = %{stable_version}-%{release}

%description -n python3-opentelemetry-exporter-otlp-proto-grpc
This library allows to export data to the OpenTelemetry Collector using the
OpenTelemetry Protocol using Protobuf over gRPC.


%package -n python3-opentelemetry-exporter-otlp-proto-http
Summary:        OpenTelemetry Collector Protobuf over HTTP Exporter
Version:        %{stable_version}

# Dependencies across subpackages should be fully-versioned. See comments
# following BuildRequires for a tabulation of such interdependencies.
Requires:       python3-opentelemetry-api = %{stable_version}-%{release}
Requires:       python3-opentelemetry-sdk = %{stable_version}-%{release}
Requires:       python3-opentelemetry-proto = %{stable_version}-%{release}

%description -n python3-opentelemetry-exporter-otlp-proto-http
This library allows to export data to the OpenTelemetry Collector using the
OpenTelemetry Protocol using Protobuf over HTTP.


%package -n python3-opentelemetry-exporter-otlp
Summary:        OpenTelemetry Collector Exporters
Version:        %{stable_version}

# Dependencies across subpackages should be fully-versioned. See comments
# following BuildRequires for a tabulation of such interdependencies.
Requires:       python3-opentelemetry-exporter-otlp-proto-grpc = %{stable_version}-%{release}

%description -n python3-opentelemetry-exporter-otlp
This library is provided as a convenience to install all supported
OpenTelemetry Collector Exporters. Currently it installs:

  • opentelemetry-exporter-otlp-proto-grpc
  • opentelemetry-exporter-otlp-proto-http

In the future, additional packages will be available:

  • opentelemetry-exporter-otlp-json-http

To avoid unnecessary dependencies, users should install the specific package
once they’ve determined their preferred serialization and protocol method.


%package -n python3-opentelemetry-exporter-prometheus
Summary:        OpenTelemetry Prometheus Exporter
Version:        %{prerel_version}

Obsoletes:      python3-opentelemetry-ext-prometheus < 1.0

Requires:       ((%{py3_dist prometheus_client} >= 0.5.0) with (%{py3_dist prometheus_client} < 1.0.0))
# Dependencies across subpackages should be fully-versioned. See comments
# following BuildRequires for a tabulation of such interdependencies.
Requires:       python3-opentelemetry-api = %{stable_version}-%{release}
Requires:       python3-opentelemetry-sdk = %{stable_version}-%{release}

%description -n python3-opentelemetry-exporter-prometheus
This library allows to export metrics data to Prometheus
(https://prometheus.io).


%package -n python3-opentelemetry-exporter-zipkin-json
Summary:        Zipkin Span JSON Exporter for OpenTelemetry
Version:        %{stable_version}

# Dependencies across subpackages should be fully-versioned. See comments
# following BuildRequires for a tabulation of such interdependencies.
Requires:       python3-opentelemetry-api = %{stable_version}-%{release}
Requires:       python3-opentelemetry-sdk = %{stable_version}-%{release}

%description -n python3-opentelemetry-exporter-zipkin-json
This library allows export of tracing data to Zipkin (https://zipkin.io/) using
JSON for serialization.


%package -n python3-opentelemetry-exporter-zipkin-proto-http
Summary:        Zipkin Span Protobuf Exporter for OpenTelemetry
Version:        %{stable_version}

# Dependencies across subpackages should be fully-versioned. See comments
# following BuildRequires for a tabulation of such interdependencies.
Requires:       python3-opentelemetry-api = %{stable_version}-%{release}
Requires:       python3-opentelemetry-sdk = %{stable_version}-%{release}
Requires:       python3-opentelemetry-exporter-zipkin-json = %{stable_version}-%{release}

%description -n python3-opentelemetry-exporter-zipkin-proto-http
This library allows export of tracing data to Zipkin (https://zipkin.io/) using
Protobuf for serialization.


%package -n python3-opentelemetry-exporter-zipkin
Summary:        Zipkin Span Exporters for OpenTelemetry
Version:        %{stable_version}

# Dependencies across subpackages should be fully-versioned. See comments
# following BuildRequires for a tabulation of such interdependencies.
Requires:       python3-opentelemetry-exporter-zipkin-json = %{stable_version}-%{release}
Requires:       python3-opentelemetry-exporter-zipkin-proto-http = %{stable_version}-%{release}

Obsoletes:      python3-opentelemetry-ext-wsgi < 1.0

%description -n python3-opentelemetry-exporter-zipkin
This library is provided as a convenience to install all supported
OpenTelemetry Zipkin Exporters. Currently it installs:
  • opentelemetry-exporter-zipkin-json
  • opentelemetry-exporter-zipkin-proto-http

In the future, additional packages may be available:
  • opentelemetry-exporter-zipkin-thrift

To avoid unnecessary dependencies, users should install the specific package
once they've determined their preferred serialization method.


%package -n python3-opentelemetry-api
Summary:        OpenTelemetry Python API
Version:        %{stable_version}

# Note that the huge number of instrumentation packages are released in
# https://github.com/open-telemetry/opentelemetry-python-contrib and are not
# currently packaged.
#
# The base opentelemetry-instrumentation package was also moved to “contrib” in
# release 1.6.1/0.25~b1. We therefore obsolete it…
Obsoletes:      python3-opentelemetry-instrumentation < 0.25~b1.1
# …and its pre-1.0 name…
Obsoletes:      python3-opentelemetry-auto-instrumentation < 1.0
# …and the pre-1.0 packages it was obsoleting. (Most of these are
# instrumentation extensions.)

# These have all been renamed and are now part of opentelemetry-python-contrib.
# They have a prerelease version number, which is less than the version number
# of the old packages, so obsoleting by version number alone is insufficient.
# It is fortunate, then, that they also have new names, and it is unlikely the
# old names will ever come back in any form.
#
# Any renamed pre-1.0 packages that remain in this repository are instead
# obsoleted by the corresponding new packages.

#   • opentelemetry-instrumentation-aiohttp-client
Obsoletes:      python3-opentelemetry-ext-aiohttp-client < 1.0
#   • opentelemetry-instrumentation-asgi
Obsoletes:      python3-opentelemetry-ext-asgi < 1.0
#   • opentelemetry-instrumentation-dbapi
Obsoletes:      python3-opentelemetry-ext-dbapi < 1.0
#   • opentelemetry-instrumentation-django
Obsoletes:      python3-opentelemetry-ext-django < 1.0
#   • opentelemetry-instrumentation-flask
Obsoletes:      python3-opentelemetry-ext-flask < 1.0
#   • opentelemetry-instrumentation-grpc
Obsoletes:      python3-opentelemetry-ext-grpc < 1.0
#   • opentelemetry-instrumentation-jinja2
Obsoletes:      python3-opentelemetry-ext-jinja2 < 1.0
#   • opentelemetry-instrumentation-mysql
Obsoletes:      python3-opentelemetry-ext-mysql < 1.0
#   • opentelemetry-instrumentation-psycopg2
Obsoletes:      python3-opentelemetry-ext-psycopg2 < 1.0
#   • opentelemetry-instrumentation-pymongo
Obsoletes:      python3-opentelemetry-ext-pymongo < 1.0
#   • opentelemetry-instrumentation-pymysql
Obsoletes:      python3-opentelemetry-ext-pymysql < 1.0
#   • opentelemetry-instrumentation-redis
Obsoletes:      python3-opentelemetry-ext-redis < 1.0
#   • opentelemetry-instrumentation-requests
Obsoletes:      python3-opentelemetry-ext-requests < 1.0
#   • opentelemetry-instrumentation-sqlalchemy
Obsoletes:      python3-opentelemetry-ext-sqlalchemy < 1.0
#   • opentelemetry-instrumentation-sqlite3
Obsoletes:      python3-opentelemetry-ext-sqlite3 < 1.0
#   • opentelemetry-instrumentation-wsgi
Obsoletes:      python3-opentelemetry-ext-wsgi < 1.0

#   • opentelemetry-exporter-datadog
Obsoletes:      python3-opentelemetry-ext-datadog < 1.0

# The opentelemetry-distro package was moved to “contrib” in release
# 1.6.1/0.25~b1.
Obsoletes:      python3-opentelemetry-distro < 0.25~b1.1
Obsoletes:      python3-opentelemetry-distro+otlp < 0.25~b1.1

%description -n python3-opentelemetry-api
%{summary}.


%package -n python3-opentelemetry-proto
Summary:        OpenTelemetry Python Proto
Version:        %{stable_version}

%description -n python3-opentelemetry-proto
%{summary}.


%package -n python3-opentelemetry-sdk
Summary:        OpenTelemetry Python SDK
Version:        %{stable_version}

# Dependencies across subpackages should be fully-versioned. See comments
# following BuildRequires for a tabulation of such interdependencies.
Requires:       python3-opentelemetry-api = %{stable_version}-%{release}
Requires:       python3-opentelemetry-semantic-conventions = %{prerel_version}-%{release}

%description -n python3-opentelemetry-sdk
%{summary}.


%if %{with prerelease}
%package -n python3-opentelemetry-semantic-conventions
Summary:        OpenTelemetry Python Semantic Conventions
Version:        %{prerel_version}

%description -n python3-opentelemetry-semantic-conventions
This library contains generated code for the semantic conventions defined by the OpenTelemetry specification.
%endif


%package -n python3-opentelemetry-propagator-b3
Summary:        OpenTelemetry B3 Propagator
Version:        %{stable_version}

# Dependencies across subpackages should be fully-versioned. See comments
# following BuildRequires for a tabulation of such interdependencies.
Requires:       python3-opentelemetry-api = %{stable_version}-%{release}

%description -n python3-opentelemetry-propagator-b3
This library provides a propagator for the B3 format.


%package -n python3-opentelemetry-propagator-jaeger
Summary:        OpenTelemetry Jaeger Propagator
Version:        %{stable_version}

# Dependencies across subpackages should be fully-versioned. See comments
# following BuildRequires for a tabulation of such interdependencies.
Requires:       python3-opentelemetry-api = %{stable_version}-%{release}

%description -n python3-opentelemetry-propagator-jaeger
This library provides a propagator for the Jaeger format.


%if %{with prerelease}
%package -n python3-opentelemetry-opentracing-shim
Summary:        OpenTracing Shim for OpenTelemetry
Version:        %{prerel_version}

Obsoletes:      python3-opentelemetry-ext-opentracing-shim < 1.0

# Dependencies across subpackages should be fully-versioned. See comments
# following BuildRequires for a tabulation of such interdependencies.
Requires:       python3-opentelemetry-api = %{stable_version}-%{release}

%description -n python3-opentelemetry-opentracing-shim
%{summary}.
%endif


%if %{with prerelease}
%package -n python3-opentelemetry-test-utils
Summary:        OpenTracing Test Utilities
Version:        %{prerel_version}

# Dependencies across subpackages should be fully-versioned. See comments
# following BuildRequires for a tabulation of such interdependencies.
Requires:       python3-opentelemetry-api = %{stable_version}-%{release}
Requires:       python3-opentelemetry-sdk = %{stable_version}-%{release}

# Subpackage was renamed upstream
Obsoletes:      python3-opentelemetry-test < 0.26~b1-1

%description -n python3-opentelemetry-test-utils
This package provides internal testing utilities for the OpenTelemetry Python
project and provides no stability or quality guarantees. Please do not use it
for anything other than writing or running tests for the OpenTelemetry Python
project (github.com/open-telemetry/opentelemetry-python).
%endif


%package doc
Summary:        Documentation for python-opentelemetry
Version:        %{stable_version}

%description doc
This package provides documentation for python-opentelemetry.


%prep
%autosetup -n opentelemetry-python-%{stable_version} -p1

%py3_shebang_fix .

# Fix a test that shells out to the unversioned Python command. This is OK
# upstream, but not in Fedora.
sed -r -i 's|shutil\.which\("python"\)|"%{python3}"|' \
    opentelemetry-sdk/tests/trace/test_trace.py

# Drop intersphinx mappings, since we can’t download remote inventories and
# can’t easily produce working hyperlinks from inventories in local
# documentation packages.
echo 'intersphinx_mapping.clear()' >> docs/conf.py


%build
# Since we will need all of the Python packages for the documentation build, we
# do a temporary install of the built packages into a local directory, and add
# it to the PYTHONPATH.
PYROOT="${PWD}/%{_vpath_builddir}/pyroot"
if [ -n "${PYTHONPATH-}" ]; then PYTHONPATH="${PYTHONPATH}:"; fi
PYTHONPATH="${PYTHONPATH-}${PYROOT}%{python3_sitelib}"
export PYTHONPATH

# See eachdist.ini:
for pkg in \
%if %{with prerelease}
    shim/opentelemetry-opentracing-shim \
    exporter/opentelemetry-exporter-opencensus \
    opentelemetry-semantic-conventions \
    tests/opentelemetry-test-utils \
%endif
    opentelemetry-sdk \
    opentelemetry-proto \
    propagator/opentelemetry-propagator-jaeger \
    propagator/opentelemetry-propagator-b3 \
    exporter/opentelemetry-exporter-zipkin-proto-http \
    exporter/opentelemetry-exporter-zipkin-json \
    exporter/opentelemetry-exporter-zipkin \
    exporter/opentelemetry-exporter-prometheus \
    exporter/opentelemetry-exporter-otlp-proto-grpc \
    exporter/opentelemetry-exporter-otlp-proto-http \
    exporter/opentelemetry-exporter-otlp \
    exporter/opentelemetry-exporter-jaeger-thrift \
    exporter/opentelemetry-exporter-jaeger-proto-grpc \
    exporter/opentelemetry-exporter-jaeger \
    opentelemetry-api
do
  pushd "${pkg}"
  %py3_build
  %{python3} %{py_setup} %{?py_setup_args} install \
      -O1 --skip-build --root "${PYROOT}"
  popd
done

# Build documentation
%if %{with doc_pdf}
%make_build -C docs latex SPHINXOPTS='%{?_smp_mflags}'
%make_build -C docs/_build/latex LATEXMKOPTS='-quiet'
%endif


%install
# See eachdist.ini:
for pkg in \
%if %{with prerelease}
    shim/opentelemetry-opentracing-shim \
    exporter/opentelemetry-exporter-opencensus \
    opentelemetry-semantic-conventions \
    tests/opentelemetry-test-utils \
%endif
    opentelemetry-sdk \
    opentelemetry-proto \
    propagator/opentelemetry-propagator-jaeger \
    propagator/opentelemetry-propagator-b3 \
    exporter/opentelemetry-exporter-zipkin-proto-http \
    exporter/opentelemetry-exporter-zipkin-json \
    exporter/opentelemetry-exporter-zipkin \
    exporter/opentelemetry-exporter-prometheus \
    exporter/opentelemetry-exporter-otlp-proto-grpc \
    exporter/opentelemetry-exporter-otlp-proto-http \
    exporter/opentelemetry-exporter-otlp \
    exporter/opentelemetry-exporter-jaeger-thrift \
    exporter/opentelemetry-exporter-jaeger-proto-grpc \
    exporter/opentelemetry-exporter-jaeger \
    opentelemetry-api
do
  pushd "${pkg}"
  %py3_install
  popd
done


%check
# Note we do not attempt to run tests for opentelemetry-test-utils, i.e.
# tests/opentelemetry-test-utils; there are none in practice, and pytest would
# indicate failure.
#
# See eachdist.ini:
for pkg in \
%if %{with prerelease}
    shim/opentelemetry-opentracing-shim \
    exporter/opentelemetry-exporter-opencensus \
    opentelemetry-semantic-conventions \
%endif
    opentelemetry-sdk \
    opentelemetry-proto \
    propagator/opentelemetry-propagator-jaeger \
    propagator/opentelemetry-propagator-b3 \
    exporter/opentelemetry-exporter-zipkin-proto-http \
    exporter/opentelemetry-exporter-zipkin-json \
    exporter/opentelemetry-exporter-zipkin \
    exporter/opentelemetry-exporter-prometheus \
    exporter/opentelemetry-exporter-otlp-proto-grpc \
    exporter/opentelemetry-exporter-otlp-proto-http \
    exporter/opentelemetry-exporter-otlp \
    exporter/opentelemetry-exporter-jaeger-thrift \
    exporter/opentelemetry-exporter-jaeger-proto-grpc \
    exporter/opentelemetry-exporter-jaeger \
    opentelemetry-api
do
  if [ "${pkg}" = 'exporter/opentelemetry-exporter-jaeger-proto-grpc' ]
  then
    # https://github.com/open-telemetry/opentelemetry-python/issues/1975
    k="${k-}${k+ and }not (TestJaegerExporter and test_export)"
    k="${k-}${k+ and }not (TestJaegerExporter and test_export_span_service_name)"
  fi
  %pytest "${pkg}" -k "${k-}"
done


%files -n python3-opentelemetry-exporter-jaeger-proto-grpc
# Note that the contents are identical to the top-level LICENSE file.
%license exporter/opentelemetry-exporter-jaeger-proto-grpc/LICENSE
%doc exporter/opentelemetry-exporter-jaeger-proto-grpc/README.rst
%doc exporter/opentelemetry-exporter-jaeger-proto-grpc/examples

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry
%{python3_sitelib}/opentelemetry/py.typed
%dir %{python3_sitelib}/opentelemetry/exporter
%dir %{python3_sitelib}/opentelemetry/exporter/jaeger
%dir %{python3_sitelib}/opentelemetry/exporter/jaeger/proto

%{python3_sitelib}/opentelemetry/exporter/jaeger/proto/grpc
%{python3_sitelib}/opentelemetry_exporter_jaeger_proto_grpc-%{stable_egginfo}


%files -n python3-opentelemetry-exporter-jaeger-thrift
# Note that the contents are identical to the top-level LICENSE file.
%license exporter/opentelemetry-exporter-jaeger-thrift/LICENSE
%doc exporter/opentelemetry-exporter-jaeger-thrift/README.rst
%doc exporter/opentelemetry-exporter-jaeger-thrift/examples

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry
%{python3_sitelib}/opentelemetry/py.typed
%dir %{python3_sitelib}/opentelemetry/exporter
%dir %{python3_sitelib}/opentelemetry/exporter/jaeger

%{python3_sitelib}/opentelemetry/exporter/jaeger/thrift
%{python3_sitelib}/opentelemetry_exporter_jaeger_thrift-%{stable_egginfo}


%files -n python3-opentelemetry-exporter-jaeger
# Note that the contents are identical to the top-level LICENSE file.
%license exporter/opentelemetry-exporter-jaeger/LICENSE
%doc exporter/opentelemetry-exporter-jaeger/README.rst

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry
%{python3_sitelib}/opentelemetry/py.typed
%dir %{python3_sitelib}/opentelemetry/exporter
%dir %{python3_sitelib}/opentelemetry/exporter/jaeger

%dir %{python3_sitelib}/opentelemetry/exporter/jaeger/__pycache__
%pycached %{python3_sitelib}/opentelemetry/exporter/jaeger/version.py
%{python3_sitelib}/opentelemetry_exporter_jaeger-%{stable_egginfo}


%if %{with prerelease}
%files -n python3-opentelemetry-exporter-opencensus
# Note that the contents are identical to the top-level LICENSE file.
%license exporter/opentelemetry-exporter-opencensus/LICENSE
%doc exporter/opentelemetry-exporter-opencensus/README.rst

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry
%{python3_sitelib}/opentelemetry/py.typed
%dir %{python3_sitelib}/opentelemetry/exporter

%{python3_sitelib}/opentelemetry/exporter/opencensus
%{python3_sitelib}/opentelemetry_exporter_opencensus-%{prerel_egginfo}
%endif


%files -n python3-opentelemetry-exporter-otlp-proto-grpc
# Note that the contents are identical to the top-level LICENSE file.
%license exporter/opentelemetry-exporter-otlp-proto-grpc/LICENSE
%doc exporter/opentelemetry-exporter-otlp-proto-grpc/README.rst

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry
%{python3_sitelib}/opentelemetry/py.typed
%dir %{python3_sitelib}/opentelemetry/exporter
%dir %{python3_sitelib}/opentelemetry/exporter/otlp
%dir %{python3_sitelib}/opentelemetry/exporter/otlp/proto

%{python3_sitelib}/opentelemetry/exporter/otlp/proto/grpc
%{python3_sitelib}/opentelemetry_exporter_otlp_proto_grpc-%{stable_egginfo}


%files -n python3-opentelemetry-exporter-otlp-proto-http
# Note that the contents are identical to the top-level LICENSE file.
%license exporter/opentelemetry-exporter-otlp-proto-http/LICENSE
%doc exporter/opentelemetry-exporter-otlp-proto-http/README.rst

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry
%{python3_sitelib}/opentelemetry/py.typed
%dir %{python3_sitelib}/opentelemetry/exporter
%dir %{python3_sitelib}/opentelemetry/exporter/otlp
%dir %{python3_sitelib}/opentelemetry/exporter/otlp/proto

%{python3_sitelib}/opentelemetry/exporter/otlp/proto/http
%{python3_sitelib}/opentelemetry_exporter_otlp_proto_http-%{stable_egginfo}


%files -n python3-opentelemetry-exporter-otlp
# Note that the contents are identical to the top-level LICENSE file.
%license exporter/opentelemetry-exporter-otlp/LICENSE
%doc exporter/opentelemetry-exporter-otlp/README.rst

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry
%{python3_sitelib}/opentelemetry/py.typed
%dir %{python3_sitelib}/opentelemetry/exporter
%dir %{python3_sitelib}/opentelemetry/exporter/otlp

%dir %{python3_sitelib}/opentelemetry/exporter/otlp/__pycache__
%pycached %{python3_sitelib}/opentelemetry/exporter/otlp/version.py
%{python3_sitelib}/opentelemetry_exporter_otlp-%{stable_egginfo}


%files -n python3-opentelemetry-exporter-prometheus
# Note that the contents are identical to the top-level LICENSE file.
%license exporter/opentelemetry-exporter-prometheus/LICENSE
%doc exporter/opentelemetry-exporter-prometheus/README.rst

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry
%{python3_sitelib}/opentelemetry/py.typed
%dir %{python3_sitelib}/opentelemetry/exporter

%{python3_sitelib}/opentelemetry/exporter/prometheus
%{python3_sitelib}/opentelemetry_exporter_prometheus-%{prerel_egginfo}


%files -n python3-opentelemetry-exporter-zipkin-json
# Note that the contents are identical to the top-level LICENSE file.
%license exporter/opentelemetry-exporter-zipkin-json/LICENSE
# Not packaged since it is a zero-length file:
#doc exporter/opentelemetry-exporter-zipkin-json/CHANGELOG.md
%doc exporter/opentelemetry-exporter-zipkin-json/README.rst

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry
%{python3_sitelib}/opentelemetry/py.typed
%dir %{python3_sitelib}/opentelemetry/exporter
%dir %{python3_sitelib}/opentelemetry/exporter/zipkin

%{python3_sitelib}/opentelemetry/exporter/zipkin/encoder
%{python3_sitelib}/opentelemetry/exporter/zipkin/json
%pycached %{python3_sitelib}/opentelemetry/exporter/zipkin/node_endpoint.py
%{python3_sitelib}/opentelemetry_exporter_zipkin_json-%{stable_egginfo}


%files -n python3-opentelemetry-exporter-zipkin-proto-http
# Note that the contents are identical to the top-level LICENSE file.
%license exporter/opentelemetry-exporter-zipkin-proto-http/LICENSE
# Not packaged since it is a zero-length file:
#doc exporter/opentelemetry-exporter-zipkin-proto-http/CHANGELOG.md
%doc exporter/opentelemetry-exporter-zipkin-proto-http/README.rst

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry
%{python3_sitelib}/opentelemetry/py.typed
%dir %{python3_sitelib}/opentelemetry/exporter
%dir %{python3_sitelib}/opentelemetry/exporter/zipkin
%dir %{python3_sitelib}/opentelemetry/exporter/zipkin/proto

%{python3_sitelib}/opentelemetry/exporter/zipkin/proto/http
%{python3_sitelib}/opentelemetry_exporter_zipkin_proto_http-%{stable_egginfo}


%files -n python3-opentelemetry-exporter-zipkin
# Note that the contents are identical to the top-level LICENSE file.
%license exporter/opentelemetry-exporter-zipkin/LICENSE
%doc exporter/opentelemetry-exporter-zipkin/README.rst

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry
%{python3_sitelib}/opentelemetry/py.typed
%dir %{python3_sitelib}/opentelemetry/exporter
%dir %{python3_sitelib}/opentelemetry/exporter/zipkin

%dir %{python3_sitelib}/opentelemetry/exporter/zipkin/__pycache__
%pycached %{python3_sitelib}/opentelemetry/exporter/zipkin/version.py
%{python3_sitelib}/opentelemetry_exporter_zipkin-%{stable_egginfo}


%files -n python3-opentelemetry-api
# Note that the contents are identical to the top-level LICENSE file.
%license opentelemetry-api/LICENSE
%doc opentelemetry-api/README.rst

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry
%{python3_sitelib}/opentelemetry/py.typed
%dir %{python3_sitelib}/opentelemetry/propagators

%{python3_sitelib}/opentelemetry/_metrics
%{python3_sitelib}/opentelemetry/attributes
%{python3_sitelib}/opentelemetry/baggage
%{python3_sitelib}/opentelemetry/context
%{python3_sitelib}/opentelemetry/propagate
%dir %{python3_sitelib}/opentelemetry/propagators/__pycache__
%pycached %{python3_sitelib}/opentelemetry/propagators/composite.py
%pycached %{python3_sitelib}/opentelemetry/propagators/textmap.py
%{python3_sitelib}/opentelemetry/trace
%{python3_sitelib}/opentelemetry/util
%dir %{python3_sitelib}/opentelemetry/__pycache__
%pycached %{python3_sitelib}/opentelemetry/environment_variables.py
%pycached %{python3_sitelib}/opentelemetry/version.py
%{python3_sitelib}/opentelemetry_api-%{stable_egginfo}


%files -n python3-opentelemetry-proto
# Note that the contents are identical to the top-level LICENSE file.
%license opentelemetry-proto/LICENSE
%doc opentelemetry-proto/README.rst

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry
%{python3_sitelib}/opentelemetry/py.typed

%{python3_sitelib}/opentelemetry/proto
%{python3_sitelib}/opentelemetry_proto-%{stable_egginfo}


%files -n python3-opentelemetry-sdk
# Note that the contents are identical to the top-level LICENSE file.
%license opentelemetry-sdk/LICENSE
%doc opentelemetry-sdk/README.rst

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry
%{python3_sitelib}/opentelemetry/py.typed

%{python3_sitelib}/opentelemetry/sdk
%{python3_sitelib}/opentelemetry_sdk-%{stable_egginfo}


%if %{with prerelease}
%files -n python3-opentelemetry-semantic-conventions
# Note that the contents are identical to the top-level LICENSE file.
%license opentelemetry-sdk/LICENSE
%doc opentelemetry-sdk/README.rst

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry
%{python3_sitelib}/opentelemetry/py.typed

%{python3_sitelib}/opentelemetry/semconv
%{python3_sitelib}/opentelemetry_semantic_conventions-%{prerel_egginfo}
%endif


%files -n python3-opentelemetry-propagator-b3
# Note that the contents are identical to the top-level LICENSE file.
%license propagator/opentelemetry-propagator-b3/LICENSE
%doc propagator/opentelemetry-propagator-b3/README.rst

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry
%{python3_sitelib}/opentelemetry/py.typed
%dir %{python3_sitelib}/opentelemetry/propagators

%{python3_sitelib}/opentelemetry/propagators/b3
%{python3_sitelib}/opentelemetry_propagator_b3-%{stable_egginfo}


%files -n python3-opentelemetry-propagator-jaeger
# Note that the contents are identical to the top-level LICENSE file.
%license propagator/opentelemetry-propagator-jaeger/LICENSE
%doc propagator/opentelemetry-propagator-jaeger/README.rst

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry
%{python3_sitelib}/opentelemetry/py.typed
%dir %{python3_sitelib}/opentelemetry/propagators

%{python3_sitelib}/opentelemetry/propagators/jaeger
%{python3_sitelib}/opentelemetry_propagator_jaeger-%{stable_egginfo}


%if %{with prerelease}
%files -n python3-opentelemetry-opentracing-shim
# Note that the contents are identical to the top-level LICENSE file.
%license shim/opentelemetry-opentracing-shim/LICENSE
%doc shim/opentelemetry-opentracing-shim/README.rst

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry
%{python3_sitelib}/opentelemetry/py.typed
%dir %{python3_sitelib}/opentelemetry/shim

%{python3_sitelib}/opentelemetry/shim/opentracing_shim
%{python3_sitelib}/opentelemetry_opentracing_shim-%{prerel_egginfo}
%endif


%if %{with prerelease}
%files -n python3-opentelemetry-test-utils
%license LICENSE
%doc tests/opentelemetry-test-utils/README.rst

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry
%{python3_sitelib}/opentelemetry/py.typed

%{python3_sitelib}/opentelemetry/test
%{python3_sitelib}/opentelemetry_test_utils-%{prerel_egginfo}
%endif


%files doc
%license LICENSE
%if %{with doc_pdf}
%doc docs/_build/latex/opentelemetrypython.pdf
%endif


%changelog
%autochangelog
