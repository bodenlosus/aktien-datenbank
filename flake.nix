{
  description = "A multi-system Python application using Nix Flakes and flake-utils";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in {
        packages.default = pkgs.python312Packages.buildPythonApplication rec {
          pname = "aktien-datenbank";
          version = "1.0";

          # Python application source
          src = ./.;

          # Add runtime dependencies
          propagatedBuildInputs = with pkgs.python312Packages; [
            numpy
            yfinance
            python-dotenv
            schedule
          ];

          # Specify the main script or entry point
          # entryPoints = {
          #   aktien-datenbank = "main:main"; # Ensure 'main.py' has a 'main()' function
          # };

          # Optional: metadata for the package
          meta = with pkgs.lib; {
            description = "A Python app that tracks stock data.";
            license = licenses.mit;
            maintainers = [ maintainers.yourname ];
          };
        };
      });
}
