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
# , pytest-depends
, pytest-asyncio
, h2
# , unasync-cli
# # docs dependencies (optional)
# , sphinx
# , furo
}:

buildPythonPackage rec {
  pname = "postgrest";
  version = "0.18.0";
  format = "pyproject";

  disabled = pythonOlder "3.9";

  src = fetchFromGitHub {
    owner = "supabase";
    repo = "postgrest-py";
    rev = "v${version}";
    hash = "sha256-HY390YaMc1FbDroR60/L6pRDUA8NGKJI6AkW0pGx3DE="; # Replace with actual hash
  };

  nativeBuildInputs = [
    poetry-core
  ];

  propagatedBuildInputs = [
    httpx
    h2
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
    # pytest-depends # not in nixpkgs currently
    pytest-asyncio
    # unasync-cli # not in nixpkgs currently
    # Optional docs dependencies
    # sphinx # not in nixpkgs currently
    # furo
  ];

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