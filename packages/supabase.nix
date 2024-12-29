{ lib
, buildPythonPackage
, fetchFromGitHub
, pythonOlder
# build-system
, poetry-core
# dependencies
, httpx
, postgrest
, realtime
, supabase_auth
, storage3
, supabase_functions
# dev-dependencies
, black
, pre-commit
, pytest
, flake8
, isort
, pytest-cov
, commitizen
, python-dotenv
, h2
# , unasync-cli
, pytest-asyncio
}:

buildPythonPackage rec {
  pname = "supabase";
  version = "2.10.0";
  format = "pyproject";
  
  disabled = pythonOlder "3.9";

  src = fetchFromGitHub {
    owner = "supabase";
    repo = "supabase-py";
    rev = "v${version}";
    hash = "sha256-FcRIBDD9tu/EdWbGIIfExOZgu611JI1O0cmPvpYDHJY="; # Replace with actual hash
  };

  nativeBuildInputs = [
    poetry-core
  ];

  propagatedBuildInputs = [
    postgrest
    realtime
    supabase_auth
    httpx
    h2
    storage3
    supabase_functions
  ];

  nativeCheckInputs = [
    pre-commit
    black
    pytest
    flake8
    isort
    pytest-cov
    commitizen
    python-dotenv
    pytest-asyncio
  ];

  # delas with the rename of supafunc and gotrue
  patchPhase = ''
    find . -type f -exec sed -i 's/supafunc/supabase_functions/g' {} +
    find . -type f -exec sed -i 's/gotrue/supabase_auth/g' {} +
  '';

  doDecheck = false;

  pythonImportsCheck = [ "supabase" ];

  # Enable pytest-asyncio
  pytestFlagsArray = [ "--asyncio-mode=auto" ];

  meta = with lib; {
    description = "Supabase client for Python";
    homepage = "https://github.com/supabase/supabase-py";
    changelog = "https://github.com/supabase/supabase-py/blob/v${version}/CHANGELOG.md";
    license = licenses.mit;
    maintainers = with maintainers; [ ]; # Add maintainers as needed
    classifiers = [
      "Programming Language :: Python :: 3"
      "License :: OSI Approved :: MIT License"
      "Operating System :: OS Independent"
    ];
  };
}