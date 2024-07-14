#!/bin/bash

species_list=(
  "Cyberman"
  "Dalek"
  "Judoon"
  "Human"
  "Ood"
  "Silence"
  "Slitheen"
  "Sontaran"
  "Time%20Lord"
  "Weeping%20Angel"
  "Zygon"
  "Vampire"
  "Peer"
)

for species in "${species_list[@]}"; do
  curl http://127.0.0.1:8888/?species="$species"
  echo ""
done