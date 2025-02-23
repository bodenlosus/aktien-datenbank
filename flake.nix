{
  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.nixpkgs.url = "nixpkgs/nixos-unstable";
  inputs.sb-py = {
    url = "github:bodenlosus/supabase-py-nix";
    inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = inputs@{ self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachSystem [ "x86_64-linux" "aarch64-linux" ] (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python3 = pkgs.python3;
        supabase = inputs.sb-py.packages.${system}.default;
        yf = python3.pkgs.callPackage ./packages/yf.nix {};

        pyproject = builtins.fromTOML (builtins.readFile ./pyproject.toml);

        pname = pyproject.project.name or "unknown-package";
        version = pyproject.project.version or "0.0.0";

        pkg = python3.pkgs.buildPythonPackage rec {
          inherit pname version;
          format = "pyproject";
          src = ./.;

          nativeBuildInputs = with python3.pkgs; [ setuptools ];

          propagatedBuildInputs = with python3.pkgs; [
            supabase
            numpy
            pandas
            yf
            python-dotenv
            schedule
          ];
        };

        editablePkg = pkg.overrideAttrs (oldAttrs: {
          nativeBuildInputs = oldAttrs.nativeBuildInputs ++ [
            (python3.pkgs.mkPythonEditablePackage {
              pname = pyproject.project.name;
              inherit (pyproject.project) scripts version;
              root = "$PWD";
            })
          ];
        });

      in {
        packages.default = pkg;

        devShells.default = pkgs.mkShell {
          venvDir = "./.venv";
          packages = with python3.pkgs; [
            supabase
            numpy
            pandas
            yf
            python-dotenv
            schedule
            alpha-vantage
            venvShellHook
          ];
          inputsFrom = [ editablePkg ];
        };
      });
}
