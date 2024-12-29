{ lib
, buildPythonPackage
, fetchFromGitHub
, pythonOlder
# build-system
, poetry-core
# runtime dependencies
, httpx
, pydantic
# dev dependencies
, pytest
, flake8
, black
, isort
, pre-commit
, pytest-cov
# , pytest-depends
, pytest-asyncio
, faker
# , unasync-cli
, pygithub
, respx
, h2
}:

buildPythonPackage rec {
  pname = "gotrue";
  version = "2.11.0";
  format = "pyproject";

  disabled = pythonOlder "3.9";

  src = fetchFromGitHub {
    owner = "supabase";
    repo = "auth-py";
    rev = "v${version}";
    hash = "sha256-qzf12GfC5Kkx/QZBDKlr7ljG1eoufstI3df8SfgNHh4="; # Replace with actual hash
  };

  nativeBuildInputs = [
    poetry-core
  ];

  propagatedBuildInputs = [
    httpx
    h2
    pydantic
  ];

  nativeCheckInputs = [
    pytest
    flake8
    black
    isort
    pre-commit
    pytest-cov
    # pytest-depends
    pytest-asyncio
    faker
    # unasync-cli
    pygithub
    respx
  ];

  pythonImportsCheck = [
    "supabase_auth"
  ];

  doCheck = false;

  # Enable pytest-asyncio
  pytestFlagsArray = [ "--asyncio-mode=auto" ];

  meta = with lib; {
    description = "Python Client Library for Supabase Auth";
    homepage = "https://github.com/supabase/auth-py";
    documentation = "https://github.com/supabase/auth-py";
    license = licenses.mit;
    maintainers = with maintainers; [ ]; # Add maintainers as needed
    classifiers = [
      "Programming Language :: Python :: 3"
      "License :: OSI Approved :: MIT License"
      "Operating System :: OS Independent"
    ];
  };
}