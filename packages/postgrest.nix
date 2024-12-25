{ lib
, buildPythonPackage
, fetchFromGitHub
, pythonOlder
# build-system
, poetry-core
# runtime dependencies
, httpx
, deprecation
, pydantic
, strenum
# dev dependencies
, pytest
, flake8
, black
, isort
, pre-commit
, pytest-cov
, pytest-depends
, pytest-asyncio
# , unasync-cli
# # docs dependencies (optional)
# , sphinx
# , furo
}:

buildPythonPackage rec {
  pname = "postgrest";
  version = "0.19.0";
  format = "pyproject";

  disabled = pythonOlder "3.9";

  src = fetchFromGitHub {
    owner = "supabase";
    repo = "postgrest-py";
    rev = "v${version}";
    hash = "sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="; # Replace with actual hash
  };

  nativeBuildInputs = [
    poetry-core
  ];

  propagatedBuildInputs = [
    (httpx.override { extras = [ "http2" ]; })
    deprecation
    pydantic
  ] ++ lib.optionals (pythonOlder "3.11") [
    strenum
  ];

  nativeCheckInputs = [
    pytest
    flake8
    black
    isort
    pre-commit
    pytest-cov
    pytest-depends
    pytest-asyncio
    # unasync-cli
    # # Optional docs dependencies
    # sphinx
    # furo
  ];

  # Handle dependency version constraints

  pythonImportsCheck = [
    "postgrest"
  ];

  doCheck = false;

  # Enable pytest-asyncio
  pytestFlagsArray = [ "--asyncio-mode=auto" ];

  meta = with lib; {
    description = "PostgREST client for Python. This library provides an ORM interface to PostgREST.";
    homepage = "https://github.com/supabase/postgrest-py";
    documentation = "https://postgrest-py.rtfd.io";
    license = licenses.mit;
    maintainers = with maintainers; [ ]; # Add maintainers as needed
    classifiers = [
      "Programming Language :: Python :: 3"
      "License :: OSI Approved :: MIT License"
      "Operating System :: OS Independent"
    ];
  };
}