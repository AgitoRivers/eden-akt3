window.EDEN_SKILL_DEMO={
  "scenarios": {
    "experienced": "10:doppio_gioco,mistral,sotto_voce,vendetta",
    "crossroads": "7:doppio_gioco,mistral",
    "beginner": "3:",
    "spent": "10:doppio_gioco,libeccio,mistral,ressac,sotto_voce,vendetta"
  },
  "profiles": {
    "10:doppio_gioco,mistral,sotto_voce,vendetta": {
      "level": 10,
      "level_max": 10,
      "xp": 0,
      "xp_next": 600,
      "skillpunkte": 2,
      "skillpunkte_gesamt": 6,
      "skillpunkte_plan": [
        {
          "level": 3,
          "punkte": 1
        },
        {
          "level": 5,
          "punkte": 1
        },
        {
          "level": 7,
          "punkte": 1
        },
        {
          "level": 9,
          "punkte": 1
        },
        {
          "level": 10,
          "punkte": 2
        }
      ],
      "hauptpfad": "Smuggler",
      "hauptpfad_info": {
        "id": "L",
        "name": "Smuggler",
        "summary": "Growing path attribute: Cunning.",
        "attribute_label": "Cunning",
        "traits": [
          "Cunning grows with this path."
        ]
      },
      "hauptpfad_prioritaet": [
        "Berserker",
        "Fighter",
        "Smuggler",
        "Marksman"
      ],
      "pfade": [
        {
          "id": "K",
          "name": "Fighter",
          "attribut": "strength",
          "attribut_label": "Strength",
          "skills": [
            {
              "id": "mistral",
              "kuerzel": "K3",
              "label": "Mistral",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage, and the enemy is shaken for 2 rounds (no protection).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "ressac",
              "kuerzel": "K5",
              "label": "Ressac",
              "stufe": 5,
              "kosten": 3,
              "text": "Answer to their special attack: a counter (×2 against a wet enemy); against a strong one they are also weakened.",
              "gelernt": false,
              "grund": null,
              "lernfolgen": {
                "before": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "after": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "changed": false,
                "tie": false,
                "attributes": []
              }
            },
            {
              "id": "libeccio",
              "kuerzel": "K7",
              "label": "Libeccio",
              "stufe": 7,
              "kosten": 2,
              "text": "For 2 rounds you take half damage, and every perfect parry shakes them.",
              "gelernt": false,
              "grund": "Needs K5 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "lame_de_fond",
              "kuerzel": "K9",
              "label": "Lame de Fond",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: ×2, against a shaken one ×3.",
              "gelernt": false,
              "grund": "Needs K7 on the same path first.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "L",
          "name": "Smuggler",
          "attribut": "cunning",
          "attribut_label": "Cunning",
          "skills": [
            {
              "id": "doppio_gioco",
              "kuerzel": "L3",
              "label": "Doppio Gioco",
              "stufe": 3,
              "kosten": 3,
              "text": "Two cuts at 70 % each.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "sotto_voce",
              "kuerzel": "L5",
              "label": "Sotto Voce",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: your next attack is a sure crit; against a strong one their hit is also halved.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "vendetta",
              "kuerzel": "L7",
              "label": "Vendetta",
              "stufe": 7,
              "kosten": 3,
              "text": "A cut at 30 %, then they bleed (not machines).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "omerta",
              "kuerzel": "L9",
              "label": "Omertà",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: crit ×2.5 (×3.5 with a sure crit), +25 % per condition, up to 4.",
              "gelernt": false,
              "grund": null,
              "lernfolgen": {
                "before": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "after": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "changed": false,
                "tie": false,
                "attributes": []
              }
            }
          ]
        },
        {
          "id": "W",
          "name": "Marksman",
          "attribut": "perception",
          "attribut_label": "Perception",
          "skills": [
            {
              "id": "point_de_mire",
              "kuerzel": "W3",
              "label": "Point de Mire",
              "stufe": 3,
              "kosten": 2,
              "text": "They are exhausted for 3 rounds (below Perception 4: until your next turn).",
              "gelernt": false,
              "grund": null,
              "lernfolgen": {
                "before": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "after": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "changed": false,
                "tie": false,
                "attributes": []
              }
            },
            {
              "id": "bonaccia",
              "kuerzel": "W5",
              "label": "Bonaccia",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: catch a strong one completely and strike back, halve a weak one and strike back at half strength (below Perception 4: only halved).",
              "gelernt": false,
              "grund": "Needs W3 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "phare",
              "kuerzel": "W7",
              "label": "Phare",
              "stufe": 7,
              "kosten": 3,
              "text": "Against a strong special attack: blinds them and they skip 1 round (2 if charged with current); below Perception 4 only at 15 % per point.",
              "gelernt": false,
              "grund": "Needs W5 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "pluie_d_etoiles",
              "kuerzel": "W9",
              "label": "Pluie d'Étoiles",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: 3 hits at 85 % (full damage against flyers).",
              "gelernt": false,
              "grund": "Needs W7 on the same path first.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "M",
          "name": "Berserker",
          "attribut": "courage",
          "attribut_label": "Courage",
          "skills": [
            {
              "id": "scirocco",
              "kuerzel": "M3",
              "label": "Scirocco",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage and one burn stack, but afterwards you are exposed.",
              "gelernt": false,
              "grund": null,
              "lernfolgen": {
                "before": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "after": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "changed": false,
                "tie": false,
                "attributes": []
              }
            },
            {
              "id": "retour",
              "kuerzel": "M5",
              "label": "Retour de Flamme",
              "stufe": 5,
              "kosten": 2,
              "text": "Charges your weapon: their next attack is met with a counter. Parry it for ×1.5 and a burn stack (×2 against a strong special attack), miss it for ×0.5.",
              "gelernt": false,
              "grund": "Needs M3 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "furia",
              "kuerzel": "M7",
              "label": "Furia",
              "stufe": 7,
              "kosten": 3,
              "text": "One hit right away, then 2 rounds at ×1.3, and every hit adds a burn stack. You catch fire yourself and cannot defend.",
              "gelernt": false,
              "grund": "Needs M5 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "vulcano",
              "kuerzel": "M9",
              "label": "Vulcano",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: one blow per burn stack on the enemy at 60 %, ignores protection and uses up every stack. You skip 1 round afterwards.",
              "gelernt": false,
              "grund": "Needs M7 on the same path first.",
              "lernfolgen": null
            }
          ]
        }
      ],
      "hinweis": "The Smuggler path comes into its own with its finisher, Omertà."
    },
    "7:doppio_gioco,mistral": {
      "level": 7,
      "level_max": 10,
      "xp": 0,
      "xp_next": 420,
      "skillpunkte": 1,
      "skillpunkte_gesamt": 6,
      "skillpunkte_plan": [
        {
          "level": 3,
          "punkte": 1
        },
        {
          "level": 5,
          "punkte": 1
        },
        {
          "level": 7,
          "punkte": 1
        },
        {
          "level": 9,
          "punkte": 1
        },
        {
          "level": 10,
          "punkte": 2
        }
      ],
      "hauptpfad": "Fighter",
      "hauptpfad_info": {
        "id": "K",
        "name": "Fighter",
        "summary": "Growing path attribute: Strength.",
        "attribute_label": "Strength",
        "traits": [
          "Strength grows with this path."
        ]
      },
      "hauptpfad_prioritaet": [
        "Berserker",
        "Fighter",
        "Smuggler",
        "Marksman"
      ],
      "pfade": [
        {
          "id": "K",
          "name": "Fighter",
          "attribut": "strength",
          "attribut_label": "Strength",
          "skills": [
            {
              "id": "mistral",
              "kuerzel": "K3",
              "label": "Mistral",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage, and the enemy is shaken for 2 rounds (no protection).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "ressac",
              "kuerzel": "K5",
              "label": "Ressac",
              "stufe": 5,
              "kosten": 3,
              "text": "Answer to their special attack: a counter (×2 against a wet enemy); against a strong one they are also weakened.",
              "gelernt": false,
              "grund": null,
              "lernfolgen": {
                "before": {
                  "id": "K",
                  "name": "Fighter",
                  "summary": "Growing path attribute: Strength.",
                  "attribute_label": "Strength",
                  "traits": [
                    "Strength grows with this path."
                  ]
                },
                "after": {
                  "id": "K",
                  "name": "Fighter",
                  "summary": "Growing path attribute: Strength.",
                  "attribute_label": "Strength",
                  "traits": [
                    "Strength grows with this path."
                  ]
                },
                "changed": false,
                "tie": false,
                "attributes": []
              }
            },
            {
              "id": "libeccio",
              "kuerzel": "K7",
              "label": "Libeccio",
              "stufe": 7,
              "kosten": 2,
              "text": "For 2 rounds you take half damage, and every perfect parry shakes them.",
              "gelernt": false,
              "grund": "Needs K5 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "lame_de_fond",
              "kuerzel": "K9",
              "label": "Lame de Fond",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: ×2, against a shaken one ×3.",
              "gelernt": false,
              "grund": "Needs K7 on the same path first.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "L",
          "name": "Smuggler",
          "attribut": "cunning",
          "attribut_label": "Cunning",
          "skills": [
            {
              "id": "doppio_gioco",
              "kuerzel": "L3",
              "label": "Doppio Gioco",
              "stufe": 3,
              "kosten": 3,
              "text": "Two cuts at 70 % each.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "sotto_voce",
              "kuerzel": "L5",
              "label": "Sotto Voce",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: your next attack is a sure crit; against a strong one their hit is also halved.",
              "gelernt": false,
              "grund": null,
              "lernfolgen": {
                "before": {
                  "id": "K",
                  "name": "Fighter",
                  "summary": "Growing path attribute: Strength.",
                  "attribute_label": "Strength",
                  "traits": [
                    "Strength grows with this path."
                  ]
                },
                "after": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "changed": true,
                "tie": false,
                "attributes": [
                  {
                    "id": "strength",
                    "label": "Strength",
                    "before": 5,
                    "after": 2
                  },
                  {
                    "id": "cunning",
                    "label": "Cunning",
                    "before": 2,
                    "after": 5
                  }
                ]
              }
            },
            {
              "id": "vendetta",
              "kuerzel": "L7",
              "label": "Vendetta",
              "stufe": 7,
              "kosten": 3,
              "text": "A cut at 30 %, then they bleed (not machines).",
              "gelernt": false,
              "grund": "Needs L5 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "omerta",
              "kuerzel": "L9",
              "label": "Omertà",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: crit ×2.5 (×3.5 with a sure crit), +25 % per condition, up to 4.",
              "gelernt": false,
              "grund": "Needs L7 on the same path first.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "W",
          "name": "Marksman",
          "attribut": "perception",
          "attribut_label": "Perception",
          "skills": [
            {
              "id": "point_de_mire",
              "kuerzel": "W3",
              "label": "Point de Mire",
              "stufe": 3,
              "kosten": 2,
              "text": "They are exhausted for 3 rounds (below Perception 4: until your next turn).",
              "gelernt": false,
              "grund": null,
              "lernfolgen": {
                "before": {
                  "id": "K",
                  "name": "Fighter",
                  "summary": "Growing path attribute: Strength.",
                  "attribute_label": "Strength",
                  "traits": [
                    "Strength grows with this path."
                  ]
                },
                "after": {
                  "id": "K",
                  "name": "Fighter",
                  "summary": "Growing path attribute: Strength.",
                  "attribute_label": "Strength",
                  "traits": [
                    "Strength grows with this path."
                  ]
                },
                "changed": false,
                "tie": true,
                "attributes": []
              }
            },
            {
              "id": "bonaccia",
              "kuerzel": "W5",
              "label": "Bonaccia",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: catch a strong one completely and strike back, halve a weak one and strike back at half strength (below Perception 4: only halved).",
              "gelernt": false,
              "grund": "Needs W3 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "phare",
              "kuerzel": "W7",
              "label": "Phare",
              "stufe": 7,
              "kosten": 3,
              "text": "Against a strong special attack: blinds them and they skip 1 round (2 if charged with current); below Perception 4 only at 15 % per point.",
              "gelernt": false,
              "grund": "Needs W5 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "pluie_d_etoiles",
              "kuerzel": "W9",
              "label": "Pluie d'Étoiles",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: 3 hits at 85 % (full damage against flyers).",
              "gelernt": false,
              "grund": "Needs W7 on the same path first.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "M",
          "name": "Berserker",
          "attribut": "courage",
          "attribut_label": "Courage",
          "skills": [
            {
              "id": "scirocco",
              "kuerzel": "M3",
              "label": "Scirocco",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage and one burn stack, but afterwards you are exposed.",
              "gelernt": false,
              "grund": null,
              "lernfolgen": {
                "before": {
                  "id": "K",
                  "name": "Fighter",
                  "summary": "Growing path attribute: Strength.",
                  "attribute_label": "Strength",
                  "traits": [
                    "Strength grows with this path."
                  ]
                },
                "after": {
                  "id": "M",
                  "name": "Berserker",
                  "summary": "Parry window −10 %; +1 stamina when a hit damages you.",
                  "attribute_label": "Courage",
                  "traits": [
                    "Courage grows with this path.",
                    "Parry window: path modifier −10 %.",
                    "+1 stamina whenever an enemy hit damages you.",
                    "Your attacks use Courage instead of Strength when it is higher."
                  ]
                },
                "changed": true,
                "tie": true,
                "attributes": [
                  {
                    "id": "strength",
                    "label": "Strength",
                    "before": 5,
                    "after": 2
                  },
                  {
                    "id": "courage",
                    "label": "Courage",
                    "before": 2,
                    "after": 5
                  }
                ]
              }
            },
            {
              "id": "retour",
              "kuerzel": "M5",
              "label": "Retour de Flamme",
              "stufe": 5,
              "kosten": 2,
              "text": "Charges your weapon: their next attack is met with a counter. Parry it for ×1.5 and a burn stack (×2 against a strong special attack), miss it for ×0.5.",
              "gelernt": false,
              "grund": "Needs M3 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "furia",
              "kuerzel": "M7",
              "label": "Furia",
              "stufe": 7,
              "kosten": 3,
              "text": "One hit right away, then 2 rounds at ×1.3, and every hit adds a burn stack. You catch fire yourself and cannot defend.",
              "gelernt": false,
              "grund": "Needs M5 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "vulcano",
              "kuerzel": "M9",
              "label": "Vulcano",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: one blow per burn stack on the enemy at 60 %, ignores protection and uses up every stack. You skip 1 round afterwards.",
              "gelernt": false,
              "grund": "Needs M7 on the same path first.",
              "lernfolgen": null
            }
          ]
        }
      ],
      "hinweis": "The Smuggler path comes into its own with its finisher, Omertà."
    },
    "3:": {
      "level": 3,
      "level_max": 10,
      "xp": 0,
      "xp_next": 180,
      "skillpunkte": 1,
      "skillpunkte_gesamt": 6,
      "skillpunkte_plan": [
        {
          "level": 3,
          "punkte": 1
        },
        {
          "level": 5,
          "punkte": 1
        },
        {
          "level": 7,
          "punkte": 1
        },
        {
          "level": 9,
          "punkte": 1
        },
        {
          "level": 10,
          "punkte": 2
        }
      ],
      "hauptpfad": null,
      "hauptpfad_info": {
        "id": null,
        "name": null,
        "summary": "",
        "attribute_label": null,
        "traits": []
      },
      "hauptpfad_prioritaet": [
        "Berserker",
        "Fighter",
        "Smuggler",
        "Marksman"
      ],
      "pfade": [
        {
          "id": "K",
          "name": "Fighter",
          "attribut": "strength",
          "attribut_label": "Strength",
          "skills": [
            {
              "id": "mistral",
              "kuerzel": "K3",
              "label": "Mistral",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage, and the enemy is shaken for 2 rounds (no protection).",
              "gelernt": false,
              "grund": null,
              "lernfolgen": {
                "before": {
                  "id": null,
                  "name": null,
                  "summary": "",
                  "attribute_label": null,
                  "traits": []
                },
                "after": {
                  "id": "K",
                  "name": "Fighter",
                  "summary": "Growing path attribute: Strength.",
                  "attribute_label": "Strength",
                  "traits": [
                    "Strength grows with this path."
                  ]
                },
                "changed": true,
                "tie": false,
                "attributes": [
                  {
                    "id": "strength",
                    "label": "Strength",
                    "before": 2,
                    "after": 3
                  }
                ]
              }
            },
            {
              "id": "ressac",
              "kuerzel": "K5",
              "label": "Ressac",
              "stufe": 5,
              "kosten": 3,
              "text": "Answer to their special attack: a counter (×2 against a wet enemy); against a strong one they are also weakened.",
              "gelernt": false,
              "grund": "Needs K3 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "libeccio",
              "kuerzel": "K7",
              "label": "Libeccio",
              "stufe": 7,
              "kosten": 2,
              "text": "For 2 rounds you take half damage, and every perfect parry shakes them.",
              "gelernt": false,
              "grund": "Needs K5 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "lame_de_fond",
              "kuerzel": "K9",
              "label": "Lame de Fond",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: ×2, against a shaken one ×3.",
              "gelernt": false,
              "grund": "Needs K7 on the same path first.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "L",
          "name": "Smuggler",
          "attribut": "cunning",
          "attribut_label": "Cunning",
          "skills": [
            {
              "id": "doppio_gioco",
              "kuerzel": "L3",
              "label": "Doppio Gioco",
              "stufe": 3,
              "kosten": 3,
              "text": "Two cuts at 70 % each.",
              "gelernt": false,
              "grund": null,
              "lernfolgen": {
                "before": {
                  "id": null,
                  "name": null,
                  "summary": "",
                  "attribute_label": null,
                  "traits": []
                },
                "after": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "changed": true,
                "tie": false,
                "attributes": [
                  {
                    "id": "cunning",
                    "label": "Cunning",
                    "before": 2,
                    "after": 3
                  }
                ]
              }
            },
            {
              "id": "sotto_voce",
              "kuerzel": "L5",
              "label": "Sotto Voce",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: your next attack is a sure crit; against a strong one their hit is also halved.",
              "gelernt": false,
              "grund": "Needs L3 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "vendetta",
              "kuerzel": "L7",
              "label": "Vendetta",
              "stufe": 7,
              "kosten": 3,
              "text": "A cut at 30 %, then they bleed (not machines).",
              "gelernt": false,
              "grund": "Needs L5 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "omerta",
              "kuerzel": "L9",
              "label": "Omertà",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: crit ×2.5 (×3.5 with a sure crit), +25 % per condition, up to 4.",
              "gelernt": false,
              "grund": "Needs L7 on the same path first.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "W",
          "name": "Marksman",
          "attribut": "perception",
          "attribut_label": "Perception",
          "skills": [
            {
              "id": "point_de_mire",
              "kuerzel": "W3",
              "label": "Point de Mire",
              "stufe": 3,
              "kosten": 2,
              "text": "They are exhausted for 3 rounds (below Perception 4: until your next turn).",
              "gelernt": false,
              "grund": null,
              "lernfolgen": {
                "before": {
                  "id": null,
                  "name": null,
                  "summary": "",
                  "attribute_label": null,
                  "traits": []
                },
                "after": {
                  "id": "W",
                  "name": "Marksman",
                  "summary": "Parry window: path bonus +10 %.",
                  "attribute_label": "Perception",
                  "traits": [
                    "Perception grows with this path.",
                    "Parry window: path bonus +10 %."
                  ]
                },
                "changed": true,
                "tie": false,
                "attributes": [
                  {
                    "id": "perception",
                    "label": "Perception",
                    "before": 2,
                    "after": 3
                  }
                ]
              }
            },
            {
              "id": "bonaccia",
              "kuerzel": "W5",
              "label": "Bonaccia",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: catch a strong one completely and strike back, halve a weak one and strike back at half strength (below Perception 4: only halved).",
              "gelernt": false,
              "grund": "Needs W3 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "phare",
              "kuerzel": "W7",
              "label": "Phare",
              "stufe": 7,
              "kosten": 3,
              "text": "Against a strong special attack: blinds them and they skip 1 round (2 if charged with current); below Perception 4 only at 15 % per point.",
              "gelernt": false,
              "grund": "Needs W5 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "pluie_d_etoiles",
              "kuerzel": "W9",
              "label": "Pluie d'Étoiles",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: 3 hits at 85 % (full damage against flyers).",
              "gelernt": false,
              "grund": "Needs W7 on the same path first.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "M",
          "name": "Berserker",
          "attribut": "courage",
          "attribut_label": "Courage",
          "skills": [
            {
              "id": "scirocco",
              "kuerzel": "M3",
              "label": "Scirocco",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage and one burn stack, but afterwards you are exposed.",
              "gelernt": false,
              "grund": null,
              "lernfolgen": {
                "before": {
                  "id": null,
                  "name": null,
                  "summary": "",
                  "attribute_label": null,
                  "traits": []
                },
                "after": {
                  "id": "M",
                  "name": "Berserker",
                  "summary": "Parry window −10 %; +1 stamina when a hit damages you.",
                  "attribute_label": "Courage",
                  "traits": [
                    "Courage grows with this path.",
                    "Parry window: path modifier −10 %.",
                    "+1 stamina whenever an enemy hit damages you.",
                    "Your attacks use Courage instead of Strength when it is higher."
                  ]
                },
                "changed": true,
                "tie": false,
                "attributes": [
                  {
                    "id": "courage",
                    "label": "Courage",
                    "before": 2,
                    "after": 3
                  }
                ]
              }
            },
            {
              "id": "retour",
              "kuerzel": "M5",
              "label": "Retour de Flamme",
              "stufe": 5,
              "kosten": 2,
              "text": "Charges your weapon: their next attack is met with a counter. Parry it for ×1.5 and a burn stack (×2 against a strong special attack), miss it for ×0.5.",
              "gelernt": false,
              "grund": "Needs M3 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "furia",
              "kuerzel": "M7",
              "label": "Furia",
              "stufe": 7,
              "kosten": 3,
              "text": "One hit right away, then 2 rounds at ×1.3, and every hit adds a burn stack. You catch fire yourself and cannot defend.",
              "gelernt": false,
              "grund": "Needs M5 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "vulcano",
              "kuerzel": "M9",
              "label": "Vulcano",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: one blow per burn stack on the enemy at 60 %, ignores protection and uses up every stack. You skip 1 round afterwards.",
              "gelernt": false,
              "grund": "Needs M7 on the same path first.",
              "lernfolgen": null
            }
          ]
        }
      ],
      "hinweis": null
    },
    "10:doppio_gioco,libeccio,mistral,ressac,sotto_voce,vendetta": {
      "level": 10,
      "level_max": 10,
      "xp": 0,
      "xp_next": 600,
      "skillpunkte": 0,
      "skillpunkte_gesamt": 6,
      "skillpunkte_plan": [
        {
          "level": 3,
          "punkte": 1
        },
        {
          "level": 5,
          "punkte": 1
        },
        {
          "level": 7,
          "punkte": 1
        },
        {
          "level": 9,
          "punkte": 1
        },
        {
          "level": 10,
          "punkte": 2
        }
      ],
      "hauptpfad": "Fighter",
      "hauptpfad_info": {
        "id": "K",
        "name": "Fighter",
        "summary": "Growing path attribute: Strength.",
        "attribute_label": "Strength",
        "traits": [
          "Strength grows with this path."
        ]
      },
      "hauptpfad_prioritaet": [
        "Berserker",
        "Fighter",
        "Smuggler",
        "Marksman"
      ],
      "pfade": [
        {
          "id": "K",
          "name": "Fighter",
          "attribut": "strength",
          "attribut_label": "Strength",
          "skills": [
            {
              "id": "mistral",
              "kuerzel": "K3",
              "label": "Mistral",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage, and the enemy is shaken for 2 rounds (no protection).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "ressac",
              "kuerzel": "K5",
              "label": "Ressac",
              "stufe": 5,
              "kosten": 3,
              "text": "Answer to their special attack: a counter (×2 against a wet enemy); against a strong one they are also weakened.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "libeccio",
              "kuerzel": "K7",
              "label": "Libeccio",
              "stufe": 7,
              "kosten": 2,
              "text": "For 2 rounds you take half damage, and every perfect parry shakes them.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "lame_de_fond",
              "kuerzel": "K9",
              "label": "Lame de Fond",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: ×2, against a shaken one ×3.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "L",
          "name": "Smuggler",
          "attribut": "cunning",
          "attribut_label": "Cunning",
          "skills": [
            {
              "id": "doppio_gioco",
              "kuerzel": "L3",
              "label": "Doppio Gioco",
              "stufe": 3,
              "kosten": 3,
              "text": "Two cuts at 70 % each.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "sotto_voce",
              "kuerzel": "L5",
              "label": "Sotto Voce",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: your next attack is a sure crit; against a strong one their hit is also halved.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "vendetta",
              "kuerzel": "L7",
              "label": "Vendetta",
              "stufe": 7,
              "kosten": 3,
              "text": "A cut at 30 %, then they bleed (not machines).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "omerta",
              "kuerzel": "L9",
              "label": "Omertà",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: crit ×2.5 (×3.5 with a sure crit), +25 % per condition, up to 4.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "W",
          "name": "Marksman",
          "attribut": "perception",
          "attribut_label": "Perception",
          "skills": [
            {
              "id": "point_de_mire",
              "kuerzel": "W3",
              "label": "Point de Mire",
              "stufe": 3,
              "kosten": 2,
              "text": "They are exhausted for 3 rounds (below Perception 4: until your next turn).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "bonaccia",
              "kuerzel": "W5",
              "label": "Bonaccia",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: catch a strong one completely and strike back, halve a weak one and strike back at half strength (below Perception 4: only halved).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "phare",
              "kuerzel": "W7",
              "label": "Phare",
              "stufe": 7,
              "kosten": 3,
              "text": "Against a strong special attack: blinds them and they skip 1 round (2 if charged with current); below Perception 4 only at 15 % per point.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "pluie_d_etoiles",
              "kuerzel": "W9",
              "label": "Pluie d'Étoiles",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: 3 hits at 85 % (full damage against flyers).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "M",
          "name": "Berserker",
          "attribut": "courage",
          "attribut_label": "Courage",
          "skills": [
            {
              "id": "scirocco",
              "kuerzel": "M3",
              "label": "Scirocco",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage and one burn stack, but afterwards you are exposed.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "retour",
              "kuerzel": "M5",
              "label": "Retour de Flamme",
              "stufe": 5,
              "kosten": 2,
              "text": "Charges your weapon: their next attack is met with a counter. Parry it for ×1.5 and a burn stack (×2 against a strong special attack), miss it for ×0.5.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "furia",
              "kuerzel": "M7",
              "label": "Furia",
              "stufe": 7,
              "kosten": 3,
              "text": "One hit right away, then 2 rounds at ×1.3, and every hit adds a burn stack. You catch fire yourself and cannot defend.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "vulcano",
              "kuerzel": "M9",
              "label": "Vulcano",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: one blow per burn stack on the enemy at 60 %, ignores protection and uses up every stack. You skip 1 round afterwards.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        }
      ],
      "hinweis": "The Smuggler path comes into its own with its finisher, Omertà."
    },
    "10:doppio_gioco,mistral,ressac,sotto_voce,vendetta": {
      "level": 10,
      "level_max": 10,
      "xp": 0,
      "xp_next": 600,
      "skillpunkte": 1,
      "skillpunkte_gesamt": 6,
      "skillpunkte_plan": [
        {
          "level": 3,
          "punkte": 1
        },
        {
          "level": 5,
          "punkte": 1
        },
        {
          "level": 7,
          "punkte": 1
        },
        {
          "level": 9,
          "punkte": 1
        },
        {
          "level": 10,
          "punkte": 2
        }
      ],
      "hauptpfad": "Smuggler",
      "hauptpfad_info": {
        "id": "L",
        "name": "Smuggler",
        "summary": "Growing path attribute: Cunning.",
        "attribute_label": "Cunning",
        "traits": [
          "Cunning grows with this path."
        ]
      },
      "hauptpfad_prioritaet": [
        "Berserker",
        "Fighter",
        "Smuggler",
        "Marksman"
      ],
      "pfade": [
        {
          "id": "K",
          "name": "Fighter",
          "attribut": "strength",
          "attribut_label": "Strength",
          "skills": [
            {
              "id": "mistral",
              "kuerzel": "K3",
              "label": "Mistral",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage, and the enemy is shaken for 2 rounds (no protection).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "ressac",
              "kuerzel": "K5",
              "label": "Ressac",
              "stufe": 5,
              "kosten": 3,
              "text": "Answer to their special attack: a counter (×2 against a wet enemy); against a strong one they are also weakened.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "libeccio",
              "kuerzel": "K7",
              "label": "Libeccio",
              "stufe": 7,
              "kosten": 2,
              "text": "For 2 rounds you take half damage, and every perfect parry shakes them.",
              "gelernt": false,
              "grund": null,
              "lernfolgen": {
                "before": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "after": {
                  "id": "K",
                  "name": "Fighter",
                  "summary": "Growing path attribute: Strength.",
                  "attribute_label": "Strength",
                  "traits": [
                    "Strength grows with this path."
                  ]
                },
                "changed": true,
                "tie": true,
                "attributes": [
                  {
                    "id": "strength",
                    "label": "Strength",
                    "before": 2,
                    "after": 5
                  },
                  {
                    "id": "cunning",
                    "label": "Cunning",
                    "before": 5,
                    "after": 2
                  }
                ]
              }
            },
            {
              "id": "lame_de_fond",
              "kuerzel": "K9",
              "label": "Lame de Fond",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: ×2, against a shaken one ×3.",
              "gelernt": false,
              "grund": "Needs K7 on the same path first.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "L",
          "name": "Smuggler",
          "attribut": "cunning",
          "attribut_label": "Cunning",
          "skills": [
            {
              "id": "doppio_gioco",
              "kuerzel": "L3",
              "label": "Doppio Gioco",
              "stufe": 3,
              "kosten": 3,
              "text": "Two cuts at 70 % each.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "sotto_voce",
              "kuerzel": "L5",
              "label": "Sotto Voce",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: your next attack is a sure crit; against a strong one their hit is also halved.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "vendetta",
              "kuerzel": "L7",
              "label": "Vendetta",
              "stufe": 7,
              "kosten": 3,
              "text": "A cut at 30 %, then they bleed (not machines).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "omerta",
              "kuerzel": "L9",
              "label": "Omertà",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: crit ×2.5 (×3.5 with a sure crit), +25 % per condition, up to 4.",
              "gelernt": false,
              "grund": null,
              "lernfolgen": {
                "before": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "after": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "changed": false,
                "tie": false,
                "attributes": []
              }
            }
          ]
        },
        {
          "id": "W",
          "name": "Marksman",
          "attribut": "perception",
          "attribut_label": "Perception",
          "skills": [
            {
              "id": "point_de_mire",
              "kuerzel": "W3",
              "label": "Point de Mire",
              "stufe": 3,
              "kosten": 2,
              "text": "They are exhausted for 3 rounds (below Perception 4: until your next turn).",
              "gelernt": false,
              "grund": null,
              "lernfolgen": {
                "before": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "after": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "changed": false,
                "tie": false,
                "attributes": []
              }
            },
            {
              "id": "bonaccia",
              "kuerzel": "W5",
              "label": "Bonaccia",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: catch a strong one completely and strike back, halve a weak one and strike back at half strength (below Perception 4: only halved).",
              "gelernt": false,
              "grund": "Needs W3 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "phare",
              "kuerzel": "W7",
              "label": "Phare",
              "stufe": 7,
              "kosten": 3,
              "text": "Against a strong special attack: blinds them and they skip 1 round (2 if charged with current); below Perception 4 only at 15 % per point.",
              "gelernt": false,
              "grund": "Needs W5 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "pluie_d_etoiles",
              "kuerzel": "W9",
              "label": "Pluie d'Étoiles",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: 3 hits at 85 % (full damage against flyers).",
              "gelernt": false,
              "grund": "Needs W7 on the same path first.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "M",
          "name": "Berserker",
          "attribut": "courage",
          "attribut_label": "Courage",
          "skills": [
            {
              "id": "scirocco",
              "kuerzel": "M3",
              "label": "Scirocco",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage and one burn stack, but afterwards you are exposed.",
              "gelernt": false,
              "grund": null,
              "lernfolgen": {
                "before": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "after": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "changed": false,
                "tie": false,
                "attributes": []
              }
            },
            {
              "id": "retour",
              "kuerzel": "M5",
              "label": "Retour de Flamme",
              "stufe": 5,
              "kosten": 2,
              "text": "Charges your weapon: their next attack is met with a counter. Parry it for ×1.5 and a burn stack (×2 against a strong special attack), miss it for ×0.5.",
              "gelernt": false,
              "grund": "Needs M3 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "furia",
              "kuerzel": "M7",
              "label": "Furia",
              "stufe": 7,
              "kosten": 3,
              "text": "One hit right away, then 2 rounds at ×1.3, and every hit adds a burn stack. You catch fire yourself and cannot defend.",
              "gelernt": false,
              "grund": "Needs M5 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "vulcano",
              "kuerzel": "M9",
              "label": "Vulcano",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: one blow per burn stack on the enemy at 60 %, ignores protection and uses up every stack. You skip 1 round afterwards.",
              "gelernt": false,
              "grund": "Needs M7 on the same path first.",
              "lernfolgen": null
            }
          ]
        }
      ],
      "hinweis": "The Smuggler path comes into its own with its finisher, Omertà."
    },
    "10:doppio_gioco,mistral,omerta,sotto_voce,vendetta": {
      "level": 10,
      "level_max": 10,
      "xp": 0,
      "xp_next": 600,
      "skillpunkte": 1,
      "skillpunkte_gesamt": 6,
      "skillpunkte_plan": [
        {
          "level": 3,
          "punkte": 1
        },
        {
          "level": 5,
          "punkte": 1
        },
        {
          "level": 7,
          "punkte": 1
        },
        {
          "level": 9,
          "punkte": 1
        },
        {
          "level": 10,
          "punkte": 2
        }
      ],
      "hauptpfad": "Smuggler",
      "hauptpfad_info": {
        "id": "L",
        "name": "Smuggler",
        "summary": "Growing path attribute: Cunning.",
        "attribute_label": "Cunning",
        "traits": [
          "Cunning grows with this path."
        ]
      },
      "hauptpfad_prioritaet": [
        "Berserker",
        "Fighter",
        "Smuggler",
        "Marksman"
      ],
      "pfade": [
        {
          "id": "K",
          "name": "Fighter",
          "attribut": "strength",
          "attribut_label": "Strength",
          "skills": [
            {
              "id": "mistral",
              "kuerzel": "K3",
              "label": "Mistral",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage, and the enemy is shaken for 2 rounds (no protection).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "ressac",
              "kuerzel": "K5",
              "label": "Ressac",
              "stufe": 5,
              "kosten": 3,
              "text": "Answer to their special attack: a counter (×2 against a wet enemy); against a strong one they are also weakened.",
              "gelernt": false,
              "grund": null,
              "lernfolgen": {
                "before": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "after": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "changed": false,
                "tie": false,
                "attributes": []
              }
            },
            {
              "id": "libeccio",
              "kuerzel": "K7",
              "label": "Libeccio",
              "stufe": 7,
              "kosten": 2,
              "text": "For 2 rounds you take half damage, and every perfect parry shakes them.",
              "gelernt": false,
              "grund": "Needs K5 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "lame_de_fond",
              "kuerzel": "K9",
              "label": "Lame de Fond",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: ×2, against a shaken one ×3.",
              "gelernt": false,
              "grund": "Needs K7 on the same path first.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "L",
          "name": "Smuggler",
          "attribut": "cunning",
          "attribut_label": "Cunning",
          "skills": [
            {
              "id": "doppio_gioco",
              "kuerzel": "L3",
              "label": "Doppio Gioco",
              "stufe": 3,
              "kosten": 3,
              "text": "Two cuts at 70 % each.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "sotto_voce",
              "kuerzel": "L5",
              "label": "Sotto Voce",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: your next attack is a sure crit; against a strong one their hit is also halved.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "vendetta",
              "kuerzel": "L7",
              "label": "Vendetta",
              "stufe": 7,
              "kosten": 3,
              "text": "A cut at 30 %, then they bleed (not machines).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "omerta",
              "kuerzel": "L9",
              "label": "Omertà",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: crit ×2.5 (×3.5 with a sure crit), +25 % per condition, up to 4.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "W",
          "name": "Marksman",
          "attribut": "perception",
          "attribut_label": "Perception",
          "skills": [
            {
              "id": "point_de_mire",
              "kuerzel": "W3",
              "label": "Point de Mire",
              "stufe": 3,
              "kosten": 2,
              "text": "They are exhausted for 3 rounds (below Perception 4: until your next turn).",
              "gelernt": false,
              "grund": null,
              "lernfolgen": {
                "before": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "after": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "changed": false,
                "tie": false,
                "attributes": []
              }
            },
            {
              "id": "bonaccia",
              "kuerzel": "W5",
              "label": "Bonaccia",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: catch a strong one completely and strike back, halve a weak one and strike back at half strength (below Perception 4: only halved).",
              "gelernt": false,
              "grund": "Needs W3 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "phare",
              "kuerzel": "W7",
              "label": "Phare",
              "stufe": 7,
              "kosten": 3,
              "text": "Against a strong special attack: blinds them and they skip 1 round (2 if charged with current); below Perception 4 only at 15 % per point.",
              "gelernt": false,
              "grund": "Needs W5 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "pluie_d_etoiles",
              "kuerzel": "W9",
              "label": "Pluie d'Étoiles",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: 3 hits at 85 % (full damage against flyers).",
              "gelernt": false,
              "grund": "Needs W7 on the same path first.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "M",
          "name": "Berserker",
          "attribut": "courage",
          "attribut_label": "Courage",
          "skills": [
            {
              "id": "scirocco",
              "kuerzel": "M3",
              "label": "Scirocco",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage and one burn stack, but afterwards you are exposed.",
              "gelernt": false,
              "grund": null,
              "lernfolgen": {
                "before": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "after": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "changed": false,
                "tie": false,
                "attributes": []
              }
            },
            {
              "id": "retour",
              "kuerzel": "M5",
              "label": "Retour de Flamme",
              "stufe": 5,
              "kosten": 2,
              "text": "Charges your weapon: their next attack is met with a counter. Parry it for ×1.5 and a burn stack (×2 against a strong special attack), miss it for ×0.5.",
              "gelernt": false,
              "grund": "Needs M3 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "furia",
              "kuerzel": "M7",
              "label": "Furia",
              "stufe": 7,
              "kosten": 3,
              "text": "One hit right away, then 2 rounds at ×1.3, and every hit adds a burn stack. You catch fire yourself and cannot defend.",
              "gelernt": false,
              "grund": "Needs M5 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "vulcano",
              "kuerzel": "M9",
              "label": "Vulcano",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: one blow per burn stack on the enemy at 60 %, ignores protection and uses up every stack. You skip 1 round afterwards.",
              "gelernt": false,
              "grund": "Needs M7 on the same path first.",
              "lernfolgen": null
            }
          ]
        }
      ],
      "hinweis": null
    },
    "10:doppio_gioco,mistral,point_de_mire,sotto_voce,vendetta": {
      "level": 10,
      "level_max": 10,
      "xp": 0,
      "xp_next": 600,
      "skillpunkte": 1,
      "skillpunkte_gesamt": 6,
      "skillpunkte_plan": [
        {
          "level": 3,
          "punkte": 1
        },
        {
          "level": 5,
          "punkte": 1
        },
        {
          "level": 7,
          "punkte": 1
        },
        {
          "level": 9,
          "punkte": 1
        },
        {
          "level": 10,
          "punkte": 2
        }
      ],
      "hauptpfad": "Smuggler",
      "hauptpfad_info": {
        "id": "L",
        "name": "Smuggler",
        "summary": "Growing path attribute: Cunning.",
        "attribute_label": "Cunning",
        "traits": [
          "Cunning grows with this path."
        ]
      },
      "hauptpfad_prioritaet": [
        "Berserker",
        "Fighter",
        "Smuggler",
        "Marksman"
      ],
      "pfade": [
        {
          "id": "K",
          "name": "Fighter",
          "attribut": "strength",
          "attribut_label": "Strength",
          "skills": [
            {
              "id": "mistral",
              "kuerzel": "K3",
              "label": "Mistral",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage, and the enemy is shaken for 2 rounds (no protection).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "ressac",
              "kuerzel": "K5",
              "label": "Ressac",
              "stufe": 5,
              "kosten": 3,
              "text": "Answer to their special attack: a counter (×2 against a wet enemy); against a strong one they are also weakened.",
              "gelernt": false,
              "grund": null,
              "lernfolgen": {
                "before": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "after": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "changed": false,
                "tie": false,
                "attributes": []
              }
            },
            {
              "id": "libeccio",
              "kuerzel": "K7",
              "label": "Libeccio",
              "stufe": 7,
              "kosten": 2,
              "text": "For 2 rounds you take half damage, and every perfect parry shakes them.",
              "gelernt": false,
              "grund": "Needs K5 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "lame_de_fond",
              "kuerzel": "K9",
              "label": "Lame de Fond",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: ×2, against a shaken one ×3.",
              "gelernt": false,
              "grund": "Needs K7 on the same path first.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "L",
          "name": "Smuggler",
          "attribut": "cunning",
          "attribut_label": "Cunning",
          "skills": [
            {
              "id": "doppio_gioco",
              "kuerzel": "L3",
              "label": "Doppio Gioco",
              "stufe": 3,
              "kosten": 3,
              "text": "Two cuts at 70 % each.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "sotto_voce",
              "kuerzel": "L5",
              "label": "Sotto Voce",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: your next attack is a sure crit; against a strong one their hit is also halved.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "vendetta",
              "kuerzel": "L7",
              "label": "Vendetta",
              "stufe": 7,
              "kosten": 3,
              "text": "A cut at 30 %, then they bleed (not machines).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "omerta",
              "kuerzel": "L9",
              "label": "Omertà",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: crit ×2.5 (×3.5 with a sure crit), +25 % per condition, up to 4.",
              "gelernt": false,
              "grund": null,
              "lernfolgen": {
                "before": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "after": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "changed": false,
                "tie": false,
                "attributes": []
              }
            }
          ]
        },
        {
          "id": "W",
          "name": "Marksman",
          "attribut": "perception",
          "attribut_label": "Perception",
          "skills": [
            {
              "id": "point_de_mire",
              "kuerzel": "W3",
              "label": "Point de Mire",
              "stufe": 3,
              "kosten": 2,
              "text": "They are exhausted for 3 rounds (below Perception 4: until your next turn).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "bonaccia",
              "kuerzel": "W5",
              "label": "Bonaccia",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: catch a strong one completely and strike back, halve a weak one and strike back at half strength (below Perception 4: only halved).",
              "gelernt": false,
              "grund": null,
              "lernfolgen": {
                "before": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "after": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "changed": false,
                "tie": false,
                "attributes": []
              }
            },
            {
              "id": "phare",
              "kuerzel": "W7",
              "label": "Phare",
              "stufe": 7,
              "kosten": 3,
              "text": "Against a strong special attack: blinds them and they skip 1 round (2 if charged with current); below Perception 4 only at 15 % per point.",
              "gelernt": false,
              "grund": "Needs W5 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "pluie_d_etoiles",
              "kuerzel": "W9",
              "label": "Pluie d'Étoiles",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: 3 hits at 85 % (full damage against flyers).",
              "gelernt": false,
              "grund": "Needs W7 on the same path first.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "M",
          "name": "Berserker",
          "attribut": "courage",
          "attribut_label": "Courage",
          "skills": [
            {
              "id": "scirocco",
              "kuerzel": "M3",
              "label": "Scirocco",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage and one burn stack, but afterwards you are exposed.",
              "gelernt": false,
              "grund": null,
              "lernfolgen": {
                "before": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "after": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "changed": false,
                "tie": false,
                "attributes": []
              }
            },
            {
              "id": "retour",
              "kuerzel": "M5",
              "label": "Retour de Flamme",
              "stufe": 5,
              "kosten": 2,
              "text": "Charges your weapon: their next attack is met with a counter. Parry it for ×1.5 and a burn stack (×2 against a strong special attack), miss it for ×0.5.",
              "gelernt": false,
              "grund": "Needs M3 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "furia",
              "kuerzel": "M7",
              "label": "Furia",
              "stufe": 7,
              "kosten": 3,
              "text": "One hit right away, then 2 rounds at ×1.3, and every hit adds a burn stack. You catch fire yourself and cannot defend.",
              "gelernt": false,
              "grund": "Needs M5 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "vulcano",
              "kuerzel": "M9",
              "label": "Vulcano",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: one blow per burn stack on the enemy at 60 %, ignores protection and uses up every stack. You skip 1 round afterwards.",
              "gelernt": false,
              "grund": "Needs M7 on the same path first.",
              "lernfolgen": null
            }
          ]
        }
      ],
      "hinweis": "The Smuggler path comes into its own with its finisher, Omertà."
    },
    "10:doppio_gioco,mistral,scirocco,sotto_voce,vendetta": {
      "level": 10,
      "level_max": 10,
      "xp": 0,
      "xp_next": 600,
      "skillpunkte": 1,
      "skillpunkte_gesamt": 6,
      "skillpunkte_plan": [
        {
          "level": 3,
          "punkte": 1
        },
        {
          "level": 5,
          "punkte": 1
        },
        {
          "level": 7,
          "punkte": 1
        },
        {
          "level": 9,
          "punkte": 1
        },
        {
          "level": 10,
          "punkte": 2
        }
      ],
      "hauptpfad": "Smuggler",
      "hauptpfad_info": {
        "id": "L",
        "name": "Smuggler",
        "summary": "Growing path attribute: Cunning.",
        "attribute_label": "Cunning",
        "traits": [
          "Cunning grows with this path."
        ]
      },
      "hauptpfad_prioritaet": [
        "Berserker",
        "Fighter",
        "Smuggler",
        "Marksman"
      ],
      "pfade": [
        {
          "id": "K",
          "name": "Fighter",
          "attribut": "strength",
          "attribut_label": "Strength",
          "skills": [
            {
              "id": "mistral",
              "kuerzel": "K3",
              "label": "Mistral",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage, and the enemy is shaken for 2 rounds (no protection).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "ressac",
              "kuerzel": "K5",
              "label": "Ressac",
              "stufe": 5,
              "kosten": 3,
              "text": "Answer to their special attack: a counter (×2 against a wet enemy); against a strong one they are also weakened.",
              "gelernt": false,
              "grund": null,
              "lernfolgen": {
                "before": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "after": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "changed": false,
                "tie": false,
                "attributes": []
              }
            },
            {
              "id": "libeccio",
              "kuerzel": "K7",
              "label": "Libeccio",
              "stufe": 7,
              "kosten": 2,
              "text": "For 2 rounds you take half damage, and every perfect parry shakes them.",
              "gelernt": false,
              "grund": "Needs K5 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "lame_de_fond",
              "kuerzel": "K9",
              "label": "Lame de Fond",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: ×2, against a shaken one ×3.",
              "gelernt": false,
              "grund": "Needs K7 on the same path first.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "L",
          "name": "Smuggler",
          "attribut": "cunning",
          "attribut_label": "Cunning",
          "skills": [
            {
              "id": "doppio_gioco",
              "kuerzel": "L3",
              "label": "Doppio Gioco",
              "stufe": 3,
              "kosten": 3,
              "text": "Two cuts at 70 % each.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "sotto_voce",
              "kuerzel": "L5",
              "label": "Sotto Voce",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: your next attack is a sure crit; against a strong one their hit is also halved.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "vendetta",
              "kuerzel": "L7",
              "label": "Vendetta",
              "stufe": 7,
              "kosten": 3,
              "text": "A cut at 30 %, then they bleed (not machines).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "omerta",
              "kuerzel": "L9",
              "label": "Omertà",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: crit ×2.5 (×3.5 with a sure crit), +25 % per condition, up to 4.",
              "gelernt": false,
              "grund": null,
              "lernfolgen": {
                "before": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "after": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "changed": false,
                "tie": false,
                "attributes": []
              }
            }
          ]
        },
        {
          "id": "W",
          "name": "Marksman",
          "attribut": "perception",
          "attribut_label": "Perception",
          "skills": [
            {
              "id": "point_de_mire",
              "kuerzel": "W3",
              "label": "Point de Mire",
              "stufe": 3,
              "kosten": 2,
              "text": "They are exhausted for 3 rounds (below Perception 4: until your next turn).",
              "gelernt": false,
              "grund": null,
              "lernfolgen": {
                "before": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "after": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "changed": false,
                "tie": false,
                "attributes": []
              }
            },
            {
              "id": "bonaccia",
              "kuerzel": "W5",
              "label": "Bonaccia",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: catch a strong one completely and strike back, halve a weak one and strike back at half strength (below Perception 4: only halved).",
              "gelernt": false,
              "grund": "Needs W3 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "phare",
              "kuerzel": "W7",
              "label": "Phare",
              "stufe": 7,
              "kosten": 3,
              "text": "Against a strong special attack: blinds them and they skip 1 round (2 if charged with current); below Perception 4 only at 15 % per point.",
              "gelernt": false,
              "grund": "Needs W5 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "pluie_d_etoiles",
              "kuerzel": "W9",
              "label": "Pluie d'Étoiles",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: 3 hits at 85 % (full damage against flyers).",
              "gelernt": false,
              "grund": "Needs W7 on the same path first.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "M",
          "name": "Berserker",
          "attribut": "courage",
          "attribut_label": "Courage",
          "skills": [
            {
              "id": "scirocco",
              "kuerzel": "M3",
              "label": "Scirocco",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage and one burn stack, but afterwards you are exposed.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "retour",
              "kuerzel": "M5",
              "label": "Retour de Flamme",
              "stufe": 5,
              "kosten": 2,
              "text": "Charges your weapon: their next attack is met with a counter. Parry it for ×1.5 and a burn stack (×2 against a strong special attack), miss it for ×0.5.",
              "gelernt": false,
              "grund": null,
              "lernfolgen": {
                "before": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "after": {
                  "id": "L",
                  "name": "Smuggler",
                  "summary": "Growing path attribute: Cunning.",
                  "attribute_label": "Cunning",
                  "traits": [
                    "Cunning grows with this path."
                  ]
                },
                "changed": false,
                "tie": false,
                "attributes": []
              }
            },
            {
              "id": "furia",
              "kuerzel": "M7",
              "label": "Furia",
              "stufe": 7,
              "kosten": 3,
              "text": "One hit right away, then 2 rounds at ×1.3, and every hit adds a burn stack. You catch fire yourself and cannot defend.",
              "gelernt": false,
              "grund": "Needs M5 on the same path first.",
              "lernfolgen": null
            },
            {
              "id": "vulcano",
              "kuerzel": "M9",
              "label": "Vulcano",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: one blow per burn stack on the enemy at 60 %, ignores protection and uses up every stack. You skip 1 round afterwards.",
              "gelernt": false,
              "grund": "Needs M7 on the same path first.",
              "lernfolgen": null
            }
          ]
        }
      ],
      "hinweis": "The Smuggler path comes into its own with its finisher, Omertà."
    },
    "7:doppio_gioco,mistral,ressac": {
      "level": 7,
      "level_max": 10,
      "xp": 0,
      "xp_next": 420,
      "skillpunkte": 0,
      "skillpunkte_gesamt": 6,
      "skillpunkte_plan": [
        {
          "level": 3,
          "punkte": 1
        },
        {
          "level": 5,
          "punkte": 1
        },
        {
          "level": 7,
          "punkte": 1
        },
        {
          "level": 9,
          "punkte": 1
        },
        {
          "level": 10,
          "punkte": 2
        }
      ],
      "hauptpfad": "Fighter",
      "hauptpfad_info": {
        "id": "K",
        "name": "Fighter",
        "summary": "Growing path attribute: Strength.",
        "attribute_label": "Strength",
        "traits": [
          "Strength grows with this path."
        ]
      },
      "hauptpfad_prioritaet": [
        "Berserker",
        "Fighter",
        "Smuggler",
        "Marksman"
      ],
      "pfade": [
        {
          "id": "K",
          "name": "Fighter",
          "attribut": "strength",
          "attribut_label": "Strength",
          "skills": [
            {
              "id": "mistral",
              "kuerzel": "K3",
              "label": "Mistral",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage, and the enemy is shaken for 2 rounds (no protection).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "ressac",
              "kuerzel": "K5",
              "label": "Ressac",
              "stufe": 5,
              "kosten": 3,
              "text": "Answer to their special attack: a counter (×2 against a wet enemy); against a strong one they are also weakened.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "libeccio",
              "kuerzel": "K7",
              "label": "Libeccio",
              "stufe": 7,
              "kosten": 2,
              "text": "For 2 rounds you take half damage, and every perfect parry shakes them.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "lame_de_fond",
              "kuerzel": "K9",
              "label": "Lame de Fond",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: ×2, against a shaken one ×3.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "L",
          "name": "Smuggler",
          "attribut": "cunning",
          "attribut_label": "Cunning",
          "skills": [
            {
              "id": "doppio_gioco",
              "kuerzel": "L3",
              "label": "Doppio Gioco",
              "stufe": 3,
              "kosten": 3,
              "text": "Two cuts at 70 % each.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "sotto_voce",
              "kuerzel": "L5",
              "label": "Sotto Voce",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: your next attack is a sure crit; against a strong one their hit is also halved.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "vendetta",
              "kuerzel": "L7",
              "label": "Vendetta",
              "stufe": 7,
              "kosten": 3,
              "text": "A cut at 30 %, then they bleed (not machines).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "omerta",
              "kuerzel": "L9",
              "label": "Omertà",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: crit ×2.5 (×3.5 with a sure crit), +25 % per condition, up to 4.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "W",
          "name": "Marksman",
          "attribut": "perception",
          "attribut_label": "Perception",
          "skills": [
            {
              "id": "point_de_mire",
              "kuerzel": "W3",
              "label": "Point de Mire",
              "stufe": 3,
              "kosten": 2,
              "text": "They are exhausted for 3 rounds (below Perception 4: until your next turn).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "bonaccia",
              "kuerzel": "W5",
              "label": "Bonaccia",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: catch a strong one completely and strike back, halve a weak one and strike back at half strength (below Perception 4: only halved).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "phare",
              "kuerzel": "W7",
              "label": "Phare",
              "stufe": 7,
              "kosten": 3,
              "text": "Against a strong special attack: blinds them and they skip 1 round (2 if charged with current); below Perception 4 only at 15 % per point.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "pluie_d_etoiles",
              "kuerzel": "W9",
              "label": "Pluie d'Étoiles",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: 3 hits at 85 % (full damage against flyers).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "M",
          "name": "Berserker",
          "attribut": "courage",
          "attribut_label": "Courage",
          "skills": [
            {
              "id": "scirocco",
              "kuerzel": "M3",
              "label": "Scirocco",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage and one burn stack, but afterwards you are exposed.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "retour",
              "kuerzel": "M5",
              "label": "Retour de Flamme",
              "stufe": 5,
              "kosten": 2,
              "text": "Charges your weapon: their next attack is met with a counter. Parry it for ×1.5 and a burn stack (×2 against a strong special attack), miss it for ×0.5.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "furia",
              "kuerzel": "M7",
              "label": "Furia",
              "stufe": 7,
              "kosten": 3,
              "text": "One hit right away, then 2 rounds at ×1.3, and every hit adds a burn stack. You catch fire yourself and cannot defend.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "vulcano",
              "kuerzel": "M9",
              "label": "Vulcano",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: one blow per burn stack on the enemy at 60 %, ignores protection and uses up every stack. You skip 1 round afterwards.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        }
      ],
      "hinweis": "The Smuggler path comes into its own with its finisher, Omertà."
    },
    "7:doppio_gioco,mistral,sotto_voce": {
      "level": 7,
      "level_max": 10,
      "xp": 0,
      "xp_next": 420,
      "skillpunkte": 0,
      "skillpunkte_gesamt": 6,
      "skillpunkte_plan": [
        {
          "level": 3,
          "punkte": 1
        },
        {
          "level": 5,
          "punkte": 1
        },
        {
          "level": 7,
          "punkte": 1
        },
        {
          "level": 9,
          "punkte": 1
        },
        {
          "level": 10,
          "punkte": 2
        }
      ],
      "hauptpfad": "Smuggler",
      "hauptpfad_info": {
        "id": "L",
        "name": "Smuggler",
        "summary": "Growing path attribute: Cunning.",
        "attribute_label": "Cunning",
        "traits": [
          "Cunning grows with this path."
        ]
      },
      "hauptpfad_prioritaet": [
        "Berserker",
        "Fighter",
        "Smuggler",
        "Marksman"
      ],
      "pfade": [
        {
          "id": "K",
          "name": "Fighter",
          "attribut": "strength",
          "attribut_label": "Strength",
          "skills": [
            {
              "id": "mistral",
              "kuerzel": "K3",
              "label": "Mistral",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage, and the enemy is shaken for 2 rounds (no protection).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "ressac",
              "kuerzel": "K5",
              "label": "Ressac",
              "stufe": 5,
              "kosten": 3,
              "text": "Answer to their special attack: a counter (×2 against a wet enemy); against a strong one they are also weakened.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "libeccio",
              "kuerzel": "K7",
              "label": "Libeccio",
              "stufe": 7,
              "kosten": 2,
              "text": "For 2 rounds you take half damage, and every perfect parry shakes them.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "lame_de_fond",
              "kuerzel": "K9",
              "label": "Lame de Fond",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: ×2, against a shaken one ×3.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "L",
          "name": "Smuggler",
          "attribut": "cunning",
          "attribut_label": "Cunning",
          "skills": [
            {
              "id": "doppio_gioco",
              "kuerzel": "L3",
              "label": "Doppio Gioco",
              "stufe": 3,
              "kosten": 3,
              "text": "Two cuts at 70 % each.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "sotto_voce",
              "kuerzel": "L5",
              "label": "Sotto Voce",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: your next attack is a sure crit; against a strong one their hit is also halved.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "vendetta",
              "kuerzel": "L7",
              "label": "Vendetta",
              "stufe": 7,
              "kosten": 3,
              "text": "A cut at 30 %, then they bleed (not machines).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "omerta",
              "kuerzel": "L9",
              "label": "Omertà",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: crit ×2.5 (×3.5 with a sure crit), +25 % per condition, up to 4.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "W",
          "name": "Marksman",
          "attribut": "perception",
          "attribut_label": "Perception",
          "skills": [
            {
              "id": "point_de_mire",
              "kuerzel": "W3",
              "label": "Point de Mire",
              "stufe": 3,
              "kosten": 2,
              "text": "They are exhausted for 3 rounds (below Perception 4: until your next turn).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "bonaccia",
              "kuerzel": "W5",
              "label": "Bonaccia",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: catch a strong one completely and strike back, halve a weak one and strike back at half strength (below Perception 4: only halved).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "phare",
              "kuerzel": "W7",
              "label": "Phare",
              "stufe": 7,
              "kosten": 3,
              "text": "Against a strong special attack: blinds them and they skip 1 round (2 if charged with current); below Perception 4 only at 15 % per point.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "pluie_d_etoiles",
              "kuerzel": "W9",
              "label": "Pluie d'Étoiles",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: 3 hits at 85 % (full damage against flyers).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "M",
          "name": "Berserker",
          "attribut": "courage",
          "attribut_label": "Courage",
          "skills": [
            {
              "id": "scirocco",
              "kuerzel": "M3",
              "label": "Scirocco",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage and one burn stack, but afterwards you are exposed.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "retour",
              "kuerzel": "M5",
              "label": "Retour de Flamme",
              "stufe": 5,
              "kosten": 2,
              "text": "Charges your weapon: their next attack is met with a counter. Parry it for ×1.5 and a burn stack (×2 against a strong special attack), miss it for ×0.5.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "furia",
              "kuerzel": "M7",
              "label": "Furia",
              "stufe": 7,
              "kosten": 3,
              "text": "One hit right away, then 2 rounds at ×1.3, and every hit adds a burn stack. You catch fire yourself and cannot defend.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "vulcano",
              "kuerzel": "M9",
              "label": "Vulcano",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: one blow per burn stack on the enemy at 60 %, ignores protection and uses up every stack. You skip 1 round afterwards.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        }
      ],
      "hinweis": "The Smuggler path comes into its own with its finisher, Omertà."
    },
    "7:doppio_gioco,mistral,point_de_mire": {
      "level": 7,
      "level_max": 10,
      "xp": 0,
      "xp_next": 420,
      "skillpunkte": 0,
      "skillpunkte_gesamt": 6,
      "skillpunkte_plan": [
        {
          "level": 3,
          "punkte": 1
        },
        {
          "level": 5,
          "punkte": 1
        },
        {
          "level": 7,
          "punkte": 1
        },
        {
          "level": 9,
          "punkte": 1
        },
        {
          "level": 10,
          "punkte": 2
        }
      ],
      "hauptpfad": "Fighter",
      "hauptpfad_info": {
        "id": "K",
        "name": "Fighter",
        "summary": "Growing path attribute: Strength.",
        "attribute_label": "Strength",
        "traits": [
          "Strength grows with this path."
        ]
      },
      "hauptpfad_prioritaet": [
        "Berserker",
        "Fighter",
        "Smuggler",
        "Marksman"
      ],
      "pfade": [
        {
          "id": "K",
          "name": "Fighter",
          "attribut": "strength",
          "attribut_label": "Strength",
          "skills": [
            {
              "id": "mistral",
              "kuerzel": "K3",
              "label": "Mistral",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage, and the enemy is shaken for 2 rounds (no protection).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "ressac",
              "kuerzel": "K5",
              "label": "Ressac",
              "stufe": 5,
              "kosten": 3,
              "text": "Answer to their special attack: a counter (×2 against a wet enemy); against a strong one they are also weakened.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "libeccio",
              "kuerzel": "K7",
              "label": "Libeccio",
              "stufe": 7,
              "kosten": 2,
              "text": "For 2 rounds you take half damage, and every perfect parry shakes them.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "lame_de_fond",
              "kuerzel": "K9",
              "label": "Lame de Fond",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: ×2, against a shaken one ×3.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "L",
          "name": "Smuggler",
          "attribut": "cunning",
          "attribut_label": "Cunning",
          "skills": [
            {
              "id": "doppio_gioco",
              "kuerzel": "L3",
              "label": "Doppio Gioco",
              "stufe": 3,
              "kosten": 3,
              "text": "Two cuts at 70 % each.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "sotto_voce",
              "kuerzel": "L5",
              "label": "Sotto Voce",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: your next attack is a sure crit; against a strong one their hit is also halved.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "vendetta",
              "kuerzel": "L7",
              "label": "Vendetta",
              "stufe": 7,
              "kosten": 3,
              "text": "A cut at 30 %, then they bleed (not machines).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "omerta",
              "kuerzel": "L9",
              "label": "Omertà",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: crit ×2.5 (×3.5 with a sure crit), +25 % per condition, up to 4.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "W",
          "name": "Marksman",
          "attribut": "perception",
          "attribut_label": "Perception",
          "skills": [
            {
              "id": "point_de_mire",
              "kuerzel": "W3",
              "label": "Point de Mire",
              "stufe": 3,
              "kosten": 2,
              "text": "They are exhausted for 3 rounds (below Perception 4: until your next turn).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "bonaccia",
              "kuerzel": "W5",
              "label": "Bonaccia",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: catch a strong one completely and strike back, halve a weak one and strike back at half strength (below Perception 4: only halved).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "phare",
              "kuerzel": "W7",
              "label": "Phare",
              "stufe": 7,
              "kosten": 3,
              "text": "Against a strong special attack: blinds them and they skip 1 round (2 if charged with current); below Perception 4 only at 15 % per point.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "pluie_d_etoiles",
              "kuerzel": "W9",
              "label": "Pluie d'Étoiles",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: 3 hits at 85 % (full damage against flyers).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "M",
          "name": "Berserker",
          "attribut": "courage",
          "attribut_label": "Courage",
          "skills": [
            {
              "id": "scirocco",
              "kuerzel": "M3",
              "label": "Scirocco",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage and one burn stack, but afterwards you are exposed.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "retour",
              "kuerzel": "M5",
              "label": "Retour de Flamme",
              "stufe": 5,
              "kosten": 2,
              "text": "Charges your weapon: their next attack is met with a counter. Parry it for ×1.5 and a burn stack (×2 against a strong special attack), miss it for ×0.5.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "furia",
              "kuerzel": "M7",
              "label": "Furia",
              "stufe": 7,
              "kosten": 3,
              "text": "One hit right away, then 2 rounds at ×1.3, and every hit adds a burn stack. You catch fire yourself and cannot defend.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "vulcano",
              "kuerzel": "M9",
              "label": "Vulcano",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: one blow per burn stack on the enemy at 60 %, ignores protection and uses up every stack. You skip 1 round afterwards.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        }
      ],
      "hinweis": "The Smuggler path comes into its own with its finisher, Omertà."
    },
    "7:doppio_gioco,mistral,scirocco": {
      "level": 7,
      "level_max": 10,
      "xp": 0,
      "xp_next": 420,
      "skillpunkte": 0,
      "skillpunkte_gesamt": 6,
      "skillpunkte_plan": [
        {
          "level": 3,
          "punkte": 1
        },
        {
          "level": 5,
          "punkte": 1
        },
        {
          "level": 7,
          "punkte": 1
        },
        {
          "level": 9,
          "punkte": 1
        },
        {
          "level": 10,
          "punkte": 2
        }
      ],
      "hauptpfad": "Berserker",
      "hauptpfad_info": {
        "id": "M",
        "name": "Berserker",
        "summary": "Parry window −10 %; +1 stamina when a hit damages you.",
        "attribute_label": "Courage",
        "traits": [
          "Courage grows with this path.",
          "Parry window: path modifier −10 %.",
          "+1 stamina whenever an enemy hit damages you.",
          "Your attacks use Courage instead of Strength when it is higher."
        ]
      },
      "hauptpfad_prioritaet": [
        "Berserker",
        "Fighter",
        "Smuggler",
        "Marksman"
      ],
      "pfade": [
        {
          "id": "K",
          "name": "Fighter",
          "attribut": "strength",
          "attribut_label": "Strength",
          "skills": [
            {
              "id": "mistral",
              "kuerzel": "K3",
              "label": "Mistral",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage, and the enemy is shaken for 2 rounds (no protection).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "ressac",
              "kuerzel": "K5",
              "label": "Ressac",
              "stufe": 5,
              "kosten": 3,
              "text": "Answer to their special attack: a counter (×2 against a wet enemy); against a strong one they are also weakened.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "libeccio",
              "kuerzel": "K7",
              "label": "Libeccio",
              "stufe": 7,
              "kosten": 2,
              "text": "For 2 rounds you take half damage, and every perfect parry shakes them.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "lame_de_fond",
              "kuerzel": "K9",
              "label": "Lame de Fond",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: ×2, against a shaken one ×3.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "L",
          "name": "Smuggler",
          "attribut": "cunning",
          "attribut_label": "Cunning",
          "skills": [
            {
              "id": "doppio_gioco",
              "kuerzel": "L3",
              "label": "Doppio Gioco",
              "stufe": 3,
              "kosten": 3,
              "text": "Two cuts at 70 % each.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "sotto_voce",
              "kuerzel": "L5",
              "label": "Sotto Voce",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: your next attack is a sure crit; against a strong one their hit is also halved.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "vendetta",
              "kuerzel": "L7",
              "label": "Vendetta",
              "stufe": 7,
              "kosten": 3,
              "text": "A cut at 30 %, then they bleed (not machines).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "omerta",
              "kuerzel": "L9",
              "label": "Omertà",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: crit ×2.5 (×3.5 with a sure crit), +25 % per condition, up to 4.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "W",
          "name": "Marksman",
          "attribut": "perception",
          "attribut_label": "Perception",
          "skills": [
            {
              "id": "point_de_mire",
              "kuerzel": "W3",
              "label": "Point de Mire",
              "stufe": 3,
              "kosten": 2,
              "text": "They are exhausted for 3 rounds (below Perception 4: until your next turn).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "bonaccia",
              "kuerzel": "W5",
              "label": "Bonaccia",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: catch a strong one completely and strike back, halve a weak one and strike back at half strength (below Perception 4: only halved).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "phare",
              "kuerzel": "W7",
              "label": "Phare",
              "stufe": 7,
              "kosten": 3,
              "text": "Against a strong special attack: blinds them and they skip 1 round (2 if charged with current); below Perception 4 only at 15 % per point.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "pluie_d_etoiles",
              "kuerzel": "W9",
              "label": "Pluie d'Étoiles",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: 3 hits at 85 % (full damage against flyers).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "M",
          "name": "Berserker",
          "attribut": "courage",
          "attribut_label": "Courage",
          "skills": [
            {
              "id": "scirocco",
              "kuerzel": "M3",
              "label": "Scirocco",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage and one burn stack, but afterwards you are exposed.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "retour",
              "kuerzel": "M5",
              "label": "Retour de Flamme",
              "stufe": 5,
              "kosten": 2,
              "text": "Charges your weapon: their next attack is met with a counter. Parry it for ×1.5 and a burn stack (×2 against a strong special attack), miss it for ×0.5.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "furia",
              "kuerzel": "M7",
              "label": "Furia",
              "stufe": 7,
              "kosten": 3,
              "text": "One hit right away, then 2 rounds at ×1.3, and every hit adds a burn stack. You catch fire yourself and cannot defend.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "vulcano",
              "kuerzel": "M9",
              "label": "Vulcano",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: one blow per burn stack on the enemy at 60 %, ignores protection and uses up every stack. You skip 1 round afterwards.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        }
      ],
      "hinweis": "The Smuggler path comes into its own with its finisher, Omertà."
    },
    "3:mistral": {
      "level": 3,
      "level_max": 10,
      "xp": 0,
      "xp_next": 180,
      "skillpunkte": 0,
      "skillpunkte_gesamt": 6,
      "skillpunkte_plan": [
        {
          "level": 3,
          "punkte": 1
        },
        {
          "level": 5,
          "punkte": 1
        },
        {
          "level": 7,
          "punkte": 1
        },
        {
          "level": 9,
          "punkte": 1
        },
        {
          "level": 10,
          "punkte": 2
        }
      ],
      "hauptpfad": "Fighter",
      "hauptpfad_info": {
        "id": "K",
        "name": "Fighter",
        "summary": "Growing path attribute: Strength.",
        "attribute_label": "Strength",
        "traits": [
          "Strength grows with this path."
        ]
      },
      "hauptpfad_prioritaet": [
        "Berserker",
        "Fighter",
        "Smuggler",
        "Marksman"
      ],
      "pfade": [
        {
          "id": "K",
          "name": "Fighter",
          "attribut": "strength",
          "attribut_label": "Strength",
          "skills": [
            {
              "id": "mistral",
              "kuerzel": "K3",
              "label": "Mistral",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage, and the enemy is shaken for 2 rounds (no protection).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "ressac",
              "kuerzel": "K5",
              "label": "Ressac",
              "stufe": 5,
              "kosten": 3,
              "text": "Answer to their special attack: a counter (×2 against a wet enemy); against a strong one they are also weakened.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "libeccio",
              "kuerzel": "K7",
              "label": "Libeccio",
              "stufe": 7,
              "kosten": 2,
              "text": "For 2 rounds you take half damage, and every perfect parry shakes them.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "lame_de_fond",
              "kuerzel": "K9",
              "label": "Lame de Fond",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: ×2, against a shaken one ×3.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "L",
          "name": "Smuggler",
          "attribut": "cunning",
          "attribut_label": "Cunning",
          "skills": [
            {
              "id": "doppio_gioco",
              "kuerzel": "L3",
              "label": "Doppio Gioco",
              "stufe": 3,
              "kosten": 3,
              "text": "Two cuts at 70 % each.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "sotto_voce",
              "kuerzel": "L5",
              "label": "Sotto Voce",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: your next attack is a sure crit; against a strong one their hit is also halved.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "vendetta",
              "kuerzel": "L7",
              "label": "Vendetta",
              "stufe": 7,
              "kosten": 3,
              "text": "A cut at 30 %, then they bleed (not machines).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "omerta",
              "kuerzel": "L9",
              "label": "Omertà",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: crit ×2.5 (×3.5 with a sure crit), +25 % per condition, up to 4.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "W",
          "name": "Marksman",
          "attribut": "perception",
          "attribut_label": "Perception",
          "skills": [
            {
              "id": "point_de_mire",
              "kuerzel": "W3",
              "label": "Point de Mire",
              "stufe": 3,
              "kosten": 2,
              "text": "They are exhausted for 3 rounds (below Perception 4: until your next turn).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "bonaccia",
              "kuerzel": "W5",
              "label": "Bonaccia",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: catch a strong one completely and strike back, halve a weak one and strike back at half strength (below Perception 4: only halved).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "phare",
              "kuerzel": "W7",
              "label": "Phare",
              "stufe": 7,
              "kosten": 3,
              "text": "Against a strong special attack: blinds them and they skip 1 round (2 if charged with current); below Perception 4 only at 15 % per point.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "pluie_d_etoiles",
              "kuerzel": "W9",
              "label": "Pluie d'Étoiles",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: 3 hits at 85 % (full damage against flyers).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "M",
          "name": "Berserker",
          "attribut": "courage",
          "attribut_label": "Courage",
          "skills": [
            {
              "id": "scirocco",
              "kuerzel": "M3",
              "label": "Scirocco",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage and one burn stack, but afterwards you are exposed.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "retour",
              "kuerzel": "M5",
              "label": "Retour de Flamme",
              "stufe": 5,
              "kosten": 2,
              "text": "Charges your weapon: their next attack is met with a counter. Parry it for ×1.5 and a burn stack (×2 against a strong special attack), miss it for ×0.5.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "furia",
              "kuerzel": "M7",
              "label": "Furia",
              "stufe": 7,
              "kosten": 3,
              "text": "One hit right away, then 2 rounds at ×1.3, and every hit adds a burn stack. You catch fire yourself and cannot defend.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "vulcano",
              "kuerzel": "M9",
              "label": "Vulcano",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: one blow per burn stack on the enemy at 60 %, ignores protection and uses up every stack. You skip 1 round afterwards.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        }
      ],
      "hinweis": null
    },
    "3:doppio_gioco": {
      "level": 3,
      "level_max": 10,
      "xp": 0,
      "xp_next": 180,
      "skillpunkte": 0,
      "skillpunkte_gesamt": 6,
      "skillpunkte_plan": [
        {
          "level": 3,
          "punkte": 1
        },
        {
          "level": 5,
          "punkte": 1
        },
        {
          "level": 7,
          "punkte": 1
        },
        {
          "level": 9,
          "punkte": 1
        },
        {
          "level": 10,
          "punkte": 2
        }
      ],
      "hauptpfad": "Smuggler",
      "hauptpfad_info": {
        "id": "L",
        "name": "Smuggler",
        "summary": "Growing path attribute: Cunning.",
        "attribute_label": "Cunning",
        "traits": [
          "Cunning grows with this path."
        ]
      },
      "hauptpfad_prioritaet": [
        "Berserker",
        "Fighter",
        "Smuggler",
        "Marksman"
      ],
      "pfade": [
        {
          "id": "K",
          "name": "Fighter",
          "attribut": "strength",
          "attribut_label": "Strength",
          "skills": [
            {
              "id": "mistral",
              "kuerzel": "K3",
              "label": "Mistral",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage, and the enemy is shaken for 2 rounds (no protection).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "ressac",
              "kuerzel": "K5",
              "label": "Ressac",
              "stufe": 5,
              "kosten": 3,
              "text": "Answer to their special attack: a counter (×2 against a wet enemy); against a strong one they are also weakened.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "libeccio",
              "kuerzel": "K7",
              "label": "Libeccio",
              "stufe": 7,
              "kosten": 2,
              "text": "For 2 rounds you take half damage, and every perfect parry shakes them.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "lame_de_fond",
              "kuerzel": "K9",
              "label": "Lame de Fond",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: ×2, against a shaken one ×3.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "L",
          "name": "Smuggler",
          "attribut": "cunning",
          "attribut_label": "Cunning",
          "skills": [
            {
              "id": "doppio_gioco",
              "kuerzel": "L3",
              "label": "Doppio Gioco",
              "stufe": 3,
              "kosten": 3,
              "text": "Two cuts at 70 % each.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "sotto_voce",
              "kuerzel": "L5",
              "label": "Sotto Voce",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: your next attack is a sure crit; against a strong one their hit is also halved.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "vendetta",
              "kuerzel": "L7",
              "label": "Vendetta",
              "stufe": 7,
              "kosten": 3,
              "text": "A cut at 30 %, then they bleed (not machines).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "omerta",
              "kuerzel": "L9",
              "label": "Omertà",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: crit ×2.5 (×3.5 with a sure crit), +25 % per condition, up to 4.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "W",
          "name": "Marksman",
          "attribut": "perception",
          "attribut_label": "Perception",
          "skills": [
            {
              "id": "point_de_mire",
              "kuerzel": "W3",
              "label": "Point de Mire",
              "stufe": 3,
              "kosten": 2,
              "text": "They are exhausted for 3 rounds (below Perception 4: until your next turn).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "bonaccia",
              "kuerzel": "W5",
              "label": "Bonaccia",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: catch a strong one completely and strike back, halve a weak one and strike back at half strength (below Perception 4: only halved).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "phare",
              "kuerzel": "W7",
              "label": "Phare",
              "stufe": 7,
              "kosten": 3,
              "text": "Against a strong special attack: blinds them and they skip 1 round (2 if charged with current); below Perception 4 only at 15 % per point.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "pluie_d_etoiles",
              "kuerzel": "W9",
              "label": "Pluie d'Étoiles",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: 3 hits at 85 % (full damage against flyers).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "M",
          "name": "Berserker",
          "attribut": "courage",
          "attribut_label": "Courage",
          "skills": [
            {
              "id": "scirocco",
              "kuerzel": "M3",
              "label": "Scirocco",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage and one burn stack, but afterwards you are exposed.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "retour",
              "kuerzel": "M5",
              "label": "Retour de Flamme",
              "stufe": 5,
              "kosten": 2,
              "text": "Charges your weapon: their next attack is met with a counter. Parry it for ×1.5 and a burn stack (×2 against a strong special attack), miss it for ×0.5.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "furia",
              "kuerzel": "M7",
              "label": "Furia",
              "stufe": 7,
              "kosten": 3,
              "text": "One hit right away, then 2 rounds at ×1.3, and every hit adds a burn stack. You catch fire yourself and cannot defend.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "vulcano",
              "kuerzel": "M9",
              "label": "Vulcano",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: one blow per burn stack on the enemy at 60 %, ignores protection and uses up every stack. You skip 1 round afterwards.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        }
      ],
      "hinweis": "The Smuggler path comes into its own with its finisher, Omertà."
    },
    "3:point_de_mire": {
      "level": 3,
      "level_max": 10,
      "xp": 0,
      "xp_next": 180,
      "skillpunkte": 0,
      "skillpunkte_gesamt": 6,
      "skillpunkte_plan": [
        {
          "level": 3,
          "punkte": 1
        },
        {
          "level": 5,
          "punkte": 1
        },
        {
          "level": 7,
          "punkte": 1
        },
        {
          "level": 9,
          "punkte": 1
        },
        {
          "level": 10,
          "punkte": 2
        }
      ],
      "hauptpfad": "Marksman",
      "hauptpfad_info": {
        "id": "W",
        "name": "Marksman",
        "summary": "Parry window: path bonus +10 %.",
        "attribute_label": "Perception",
        "traits": [
          "Perception grows with this path.",
          "Parry window: path bonus +10 %."
        ]
      },
      "hauptpfad_prioritaet": [
        "Berserker",
        "Fighter",
        "Smuggler",
        "Marksman"
      ],
      "pfade": [
        {
          "id": "K",
          "name": "Fighter",
          "attribut": "strength",
          "attribut_label": "Strength",
          "skills": [
            {
              "id": "mistral",
              "kuerzel": "K3",
              "label": "Mistral",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage, and the enemy is shaken for 2 rounds (no protection).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "ressac",
              "kuerzel": "K5",
              "label": "Ressac",
              "stufe": 5,
              "kosten": 3,
              "text": "Answer to their special attack: a counter (×2 against a wet enemy); against a strong one they are also weakened.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "libeccio",
              "kuerzel": "K7",
              "label": "Libeccio",
              "stufe": 7,
              "kosten": 2,
              "text": "For 2 rounds you take half damage, and every perfect parry shakes them.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "lame_de_fond",
              "kuerzel": "K9",
              "label": "Lame de Fond",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: ×2, against a shaken one ×3.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "L",
          "name": "Smuggler",
          "attribut": "cunning",
          "attribut_label": "Cunning",
          "skills": [
            {
              "id": "doppio_gioco",
              "kuerzel": "L3",
              "label": "Doppio Gioco",
              "stufe": 3,
              "kosten": 3,
              "text": "Two cuts at 70 % each.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "sotto_voce",
              "kuerzel": "L5",
              "label": "Sotto Voce",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: your next attack is a sure crit; against a strong one their hit is also halved.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "vendetta",
              "kuerzel": "L7",
              "label": "Vendetta",
              "stufe": 7,
              "kosten": 3,
              "text": "A cut at 30 %, then they bleed (not machines).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "omerta",
              "kuerzel": "L9",
              "label": "Omertà",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: crit ×2.5 (×3.5 with a sure crit), +25 % per condition, up to 4.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "W",
          "name": "Marksman",
          "attribut": "perception",
          "attribut_label": "Perception",
          "skills": [
            {
              "id": "point_de_mire",
              "kuerzel": "W3",
              "label": "Point de Mire",
              "stufe": 3,
              "kosten": 2,
              "text": "They are exhausted for 3 rounds (below Perception 4: until your next turn).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "bonaccia",
              "kuerzel": "W5",
              "label": "Bonaccia",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: catch a strong one completely and strike back, halve a weak one and strike back at half strength (below Perception 4: only halved).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "phare",
              "kuerzel": "W7",
              "label": "Phare",
              "stufe": 7,
              "kosten": 3,
              "text": "Against a strong special attack: blinds them and they skip 1 round (2 if charged with current); below Perception 4 only at 15 % per point.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "pluie_d_etoiles",
              "kuerzel": "W9",
              "label": "Pluie d'Étoiles",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: 3 hits at 85 % (full damage against flyers).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "M",
          "name": "Berserker",
          "attribut": "courage",
          "attribut_label": "Courage",
          "skills": [
            {
              "id": "scirocco",
              "kuerzel": "M3",
              "label": "Scirocco",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage and one burn stack, but afterwards you are exposed.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "retour",
              "kuerzel": "M5",
              "label": "Retour de Flamme",
              "stufe": 5,
              "kosten": 2,
              "text": "Charges your weapon: their next attack is met with a counter. Parry it for ×1.5 and a burn stack (×2 against a strong special attack), miss it for ×0.5.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "furia",
              "kuerzel": "M7",
              "label": "Furia",
              "stufe": 7,
              "kosten": 3,
              "text": "One hit right away, then 2 rounds at ×1.3, and every hit adds a burn stack. You catch fire yourself and cannot defend.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "vulcano",
              "kuerzel": "M9",
              "label": "Vulcano",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: one blow per burn stack on the enemy at 60 %, ignores protection and uses up every stack. You skip 1 round afterwards.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        }
      ],
      "hinweis": null
    },
    "3:scirocco": {
      "level": 3,
      "level_max": 10,
      "xp": 0,
      "xp_next": 180,
      "skillpunkte": 0,
      "skillpunkte_gesamt": 6,
      "skillpunkte_plan": [
        {
          "level": 3,
          "punkte": 1
        },
        {
          "level": 5,
          "punkte": 1
        },
        {
          "level": 7,
          "punkte": 1
        },
        {
          "level": 9,
          "punkte": 1
        },
        {
          "level": 10,
          "punkte": 2
        }
      ],
      "hauptpfad": "Berserker",
      "hauptpfad_info": {
        "id": "M",
        "name": "Berserker",
        "summary": "Parry window −10 %; +1 stamina when a hit damages you.",
        "attribute_label": "Courage",
        "traits": [
          "Courage grows with this path.",
          "Parry window: path modifier −10 %.",
          "+1 stamina whenever an enemy hit damages you.",
          "Your attacks use Courage instead of Strength when it is higher."
        ]
      },
      "hauptpfad_prioritaet": [
        "Berserker",
        "Fighter",
        "Smuggler",
        "Marksman"
      ],
      "pfade": [
        {
          "id": "K",
          "name": "Fighter",
          "attribut": "strength",
          "attribut_label": "Strength",
          "skills": [
            {
              "id": "mistral",
              "kuerzel": "K3",
              "label": "Mistral",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage, and the enemy is shaken for 2 rounds (no protection).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "ressac",
              "kuerzel": "K5",
              "label": "Ressac",
              "stufe": 5,
              "kosten": 3,
              "text": "Answer to their special attack: a counter (×2 against a wet enemy); against a strong one they are also weakened.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "libeccio",
              "kuerzel": "K7",
              "label": "Libeccio",
              "stufe": 7,
              "kosten": 2,
              "text": "For 2 rounds you take half damage, and every perfect parry shakes them.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "lame_de_fond",
              "kuerzel": "K9",
              "label": "Lame de Fond",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: ×2, against a shaken one ×3.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "L",
          "name": "Smuggler",
          "attribut": "cunning",
          "attribut_label": "Cunning",
          "skills": [
            {
              "id": "doppio_gioco",
              "kuerzel": "L3",
              "label": "Doppio Gioco",
              "stufe": 3,
              "kosten": 3,
              "text": "Two cuts at 70 % each.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "sotto_voce",
              "kuerzel": "L5",
              "label": "Sotto Voce",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: your next attack is a sure crit; against a strong one their hit is also halved.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "vendetta",
              "kuerzel": "L7",
              "label": "Vendetta",
              "stufe": 7,
              "kosten": 3,
              "text": "A cut at 30 %, then they bleed (not machines).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "omerta",
              "kuerzel": "L9",
              "label": "Omertà",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: crit ×2.5 (×3.5 with a sure crit), +25 % per condition, up to 4.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "W",
          "name": "Marksman",
          "attribut": "perception",
          "attribut_label": "Perception",
          "skills": [
            {
              "id": "point_de_mire",
              "kuerzel": "W3",
              "label": "Point de Mire",
              "stufe": 3,
              "kosten": 2,
              "text": "They are exhausted for 3 rounds (below Perception 4: until your next turn).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "bonaccia",
              "kuerzel": "W5",
              "label": "Bonaccia",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: catch a strong one completely and strike back, halve a weak one and strike back at half strength (below Perception 4: only halved).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "phare",
              "kuerzel": "W7",
              "label": "Phare",
              "stufe": 7,
              "kosten": 3,
              "text": "Against a strong special attack: blinds them and they skip 1 round (2 if charged with current); below Perception 4 only at 15 % per point.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "pluie_d_etoiles",
              "kuerzel": "W9",
              "label": "Pluie d'Étoiles",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: 3 hits at 85 % (full damage against flyers).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "M",
          "name": "Berserker",
          "attribut": "courage",
          "attribut_label": "Courage",
          "skills": [
            {
              "id": "scirocco",
              "kuerzel": "M3",
              "label": "Scirocco",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage and one burn stack, but afterwards you are exposed.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "retour",
              "kuerzel": "M5",
              "label": "Retour de Flamme",
              "stufe": 5,
              "kosten": 2,
              "text": "Charges your weapon: their next attack is met with a counter. Parry it for ×1.5 and a burn stack (×2 against a strong special attack), miss it for ×0.5.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "furia",
              "kuerzel": "M7",
              "label": "Furia",
              "stufe": 7,
              "kosten": 3,
              "text": "One hit right away, then 2 rounds at ×1.3, and every hit adds a burn stack. You catch fire yourself and cannot defend.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "vulcano",
              "kuerzel": "M9",
              "label": "Vulcano",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: one blow per burn stack on the enemy at 60 %, ignores protection and uses up every stack. You skip 1 round afterwards.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        }
      ],
      "hinweis": null
    },
    "10:doppio_gioco,mistral,omerta,ressac,sotto_voce,vendetta": {
      "level": 10,
      "level_max": 10,
      "xp": 0,
      "xp_next": 600,
      "skillpunkte": 0,
      "skillpunkte_gesamt": 6,
      "skillpunkte_plan": [
        {
          "level": 3,
          "punkte": 1
        },
        {
          "level": 5,
          "punkte": 1
        },
        {
          "level": 7,
          "punkte": 1
        },
        {
          "level": 9,
          "punkte": 1
        },
        {
          "level": 10,
          "punkte": 2
        }
      ],
      "hauptpfad": "Smuggler",
      "hauptpfad_info": {
        "id": "L",
        "name": "Smuggler",
        "summary": "Growing path attribute: Cunning.",
        "attribute_label": "Cunning",
        "traits": [
          "Cunning grows with this path."
        ]
      },
      "hauptpfad_prioritaet": [
        "Berserker",
        "Fighter",
        "Smuggler",
        "Marksman"
      ],
      "pfade": [
        {
          "id": "K",
          "name": "Fighter",
          "attribut": "strength",
          "attribut_label": "Strength",
          "skills": [
            {
              "id": "mistral",
              "kuerzel": "K3",
              "label": "Mistral",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage, and the enemy is shaken for 2 rounds (no protection).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "ressac",
              "kuerzel": "K5",
              "label": "Ressac",
              "stufe": 5,
              "kosten": 3,
              "text": "Answer to their special attack: a counter (×2 against a wet enemy); against a strong one they are also weakened.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "libeccio",
              "kuerzel": "K7",
              "label": "Libeccio",
              "stufe": 7,
              "kosten": 2,
              "text": "For 2 rounds you take half damage, and every perfect parry shakes them.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "lame_de_fond",
              "kuerzel": "K9",
              "label": "Lame de Fond",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: ×2, against a shaken one ×3.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "L",
          "name": "Smuggler",
          "attribut": "cunning",
          "attribut_label": "Cunning",
          "skills": [
            {
              "id": "doppio_gioco",
              "kuerzel": "L3",
              "label": "Doppio Gioco",
              "stufe": 3,
              "kosten": 3,
              "text": "Two cuts at 70 % each.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "sotto_voce",
              "kuerzel": "L5",
              "label": "Sotto Voce",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: your next attack is a sure crit; against a strong one their hit is also halved.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "vendetta",
              "kuerzel": "L7",
              "label": "Vendetta",
              "stufe": 7,
              "kosten": 3,
              "text": "A cut at 30 %, then they bleed (not machines).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "omerta",
              "kuerzel": "L9",
              "label": "Omertà",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: crit ×2.5 (×3.5 with a sure crit), +25 % per condition, up to 4.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "W",
          "name": "Marksman",
          "attribut": "perception",
          "attribut_label": "Perception",
          "skills": [
            {
              "id": "point_de_mire",
              "kuerzel": "W3",
              "label": "Point de Mire",
              "stufe": 3,
              "kosten": 2,
              "text": "They are exhausted for 3 rounds (below Perception 4: until your next turn).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "bonaccia",
              "kuerzel": "W5",
              "label": "Bonaccia",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: catch a strong one completely and strike back, halve a weak one and strike back at half strength (below Perception 4: only halved).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "phare",
              "kuerzel": "W7",
              "label": "Phare",
              "stufe": 7,
              "kosten": 3,
              "text": "Against a strong special attack: blinds them and they skip 1 round (2 if charged with current); below Perception 4 only at 15 % per point.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "pluie_d_etoiles",
              "kuerzel": "W9",
              "label": "Pluie d'Étoiles",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: 3 hits at 85 % (full damage against flyers).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "M",
          "name": "Berserker",
          "attribut": "courage",
          "attribut_label": "Courage",
          "skills": [
            {
              "id": "scirocco",
              "kuerzel": "M3",
              "label": "Scirocco",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage and one burn stack, but afterwards you are exposed.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "retour",
              "kuerzel": "M5",
              "label": "Retour de Flamme",
              "stufe": 5,
              "kosten": 2,
              "text": "Charges your weapon: their next attack is met with a counter. Parry it for ×1.5 and a burn stack (×2 against a strong special attack), miss it for ×0.5.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "furia",
              "kuerzel": "M7",
              "label": "Furia",
              "stufe": 7,
              "kosten": 3,
              "text": "One hit right away, then 2 rounds at ×1.3, and every hit adds a burn stack. You catch fire yourself and cannot defend.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "vulcano",
              "kuerzel": "M9",
              "label": "Vulcano",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: one blow per burn stack on the enemy at 60 %, ignores protection and uses up every stack. You skip 1 round afterwards.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        }
      ],
      "hinweis": null
    },
    "10:doppio_gioco,mistral,point_de_mire,ressac,sotto_voce,vendetta": {
      "level": 10,
      "level_max": 10,
      "xp": 0,
      "xp_next": 600,
      "skillpunkte": 0,
      "skillpunkte_gesamt": 6,
      "skillpunkte_plan": [
        {
          "level": 3,
          "punkte": 1
        },
        {
          "level": 5,
          "punkte": 1
        },
        {
          "level": 7,
          "punkte": 1
        },
        {
          "level": 9,
          "punkte": 1
        },
        {
          "level": 10,
          "punkte": 2
        }
      ],
      "hauptpfad": "Smuggler",
      "hauptpfad_info": {
        "id": "L",
        "name": "Smuggler",
        "summary": "Growing path attribute: Cunning.",
        "attribute_label": "Cunning",
        "traits": [
          "Cunning grows with this path."
        ]
      },
      "hauptpfad_prioritaet": [
        "Berserker",
        "Fighter",
        "Smuggler",
        "Marksman"
      ],
      "pfade": [
        {
          "id": "K",
          "name": "Fighter",
          "attribut": "strength",
          "attribut_label": "Strength",
          "skills": [
            {
              "id": "mistral",
              "kuerzel": "K3",
              "label": "Mistral",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage, and the enemy is shaken for 2 rounds (no protection).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "ressac",
              "kuerzel": "K5",
              "label": "Ressac",
              "stufe": 5,
              "kosten": 3,
              "text": "Answer to their special attack: a counter (×2 against a wet enemy); against a strong one they are also weakened.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "libeccio",
              "kuerzel": "K7",
              "label": "Libeccio",
              "stufe": 7,
              "kosten": 2,
              "text": "For 2 rounds you take half damage, and every perfect parry shakes them.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "lame_de_fond",
              "kuerzel": "K9",
              "label": "Lame de Fond",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: ×2, against a shaken one ×3.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "L",
          "name": "Smuggler",
          "attribut": "cunning",
          "attribut_label": "Cunning",
          "skills": [
            {
              "id": "doppio_gioco",
              "kuerzel": "L3",
              "label": "Doppio Gioco",
              "stufe": 3,
              "kosten": 3,
              "text": "Two cuts at 70 % each.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "sotto_voce",
              "kuerzel": "L5",
              "label": "Sotto Voce",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: your next attack is a sure crit; against a strong one their hit is also halved.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "vendetta",
              "kuerzel": "L7",
              "label": "Vendetta",
              "stufe": 7,
              "kosten": 3,
              "text": "A cut at 30 %, then they bleed (not machines).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "omerta",
              "kuerzel": "L9",
              "label": "Omertà",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: crit ×2.5 (×3.5 with a sure crit), +25 % per condition, up to 4.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "W",
          "name": "Marksman",
          "attribut": "perception",
          "attribut_label": "Perception",
          "skills": [
            {
              "id": "point_de_mire",
              "kuerzel": "W3",
              "label": "Point de Mire",
              "stufe": 3,
              "kosten": 2,
              "text": "They are exhausted for 3 rounds (below Perception 4: until your next turn).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "bonaccia",
              "kuerzel": "W5",
              "label": "Bonaccia",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: catch a strong one completely and strike back, halve a weak one and strike back at half strength (below Perception 4: only halved).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "phare",
              "kuerzel": "W7",
              "label": "Phare",
              "stufe": 7,
              "kosten": 3,
              "text": "Against a strong special attack: blinds them and they skip 1 round (2 if charged with current); below Perception 4 only at 15 % per point.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "pluie_d_etoiles",
              "kuerzel": "W9",
              "label": "Pluie d'Étoiles",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: 3 hits at 85 % (full damage against flyers).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "M",
          "name": "Berserker",
          "attribut": "courage",
          "attribut_label": "Courage",
          "skills": [
            {
              "id": "scirocco",
              "kuerzel": "M3",
              "label": "Scirocco",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage and one burn stack, but afterwards you are exposed.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "retour",
              "kuerzel": "M5",
              "label": "Retour de Flamme",
              "stufe": 5,
              "kosten": 2,
              "text": "Charges your weapon: their next attack is met with a counter. Parry it for ×1.5 and a burn stack (×2 against a strong special attack), miss it for ×0.5.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "furia",
              "kuerzel": "M7",
              "label": "Furia",
              "stufe": 7,
              "kosten": 3,
              "text": "One hit right away, then 2 rounds at ×1.3, and every hit adds a burn stack. You catch fire yourself and cannot defend.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "vulcano",
              "kuerzel": "M9",
              "label": "Vulcano",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: one blow per burn stack on the enemy at 60 %, ignores protection and uses up every stack. You skip 1 round afterwards.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        }
      ],
      "hinweis": "The Smuggler path comes into its own with its finisher, Omertà."
    },
    "10:doppio_gioco,mistral,ressac,scirocco,sotto_voce,vendetta": {
      "level": 10,
      "level_max": 10,
      "xp": 0,
      "xp_next": 600,
      "skillpunkte": 0,
      "skillpunkte_gesamt": 6,
      "skillpunkte_plan": [
        {
          "level": 3,
          "punkte": 1
        },
        {
          "level": 5,
          "punkte": 1
        },
        {
          "level": 7,
          "punkte": 1
        },
        {
          "level": 9,
          "punkte": 1
        },
        {
          "level": 10,
          "punkte": 2
        }
      ],
      "hauptpfad": "Smuggler",
      "hauptpfad_info": {
        "id": "L",
        "name": "Smuggler",
        "summary": "Growing path attribute: Cunning.",
        "attribute_label": "Cunning",
        "traits": [
          "Cunning grows with this path."
        ]
      },
      "hauptpfad_prioritaet": [
        "Berserker",
        "Fighter",
        "Smuggler",
        "Marksman"
      ],
      "pfade": [
        {
          "id": "K",
          "name": "Fighter",
          "attribut": "strength",
          "attribut_label": "Strength",
          "skills": [
            {
              "id": "mistral",
              "kuerzel": "K3",
              "label": "Mistral",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage, and the enemy is shaken for 2 rounds (no protection).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "ressac",
              "kuerzel": "K5",
              "label": "Ressac",
              "stufe": 5,
              "kosten": 3,
              "text": "Answer to their special attack: a counter (×2 against a wet enemy); against a strong one they are also weakened.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "libeccio",
              "kuerzel": "K7",
              "label": "Libeccio",
              "stufe": 7,
              "kosten": 2,
              "text": "For 2 rounds you take half damage, and every perfect parry shakes them.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "lame_de_fond",
              "kuerzel": "K9",
              "label": "Lame de Fond",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: ×2, against a shaken one ×3.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "L",
          "name": "Smuggler",
          "attribut": "cunning",
          "attribut_label": "Cunning",
          "skills": [
            {
              "id": "doppio_gioco",
              "kuerzel": "L3",
              "label": "Doppio Gioco",
              "stufe": 3,
              "kosten": 3,
              "text": "Two cuts at 70 % each.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "sotto_voce",
              "kuerzel": "L5",
              "label": "Sotto Voce",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: your next attack is a sure crit; against a strong one their hit is also halved.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "vendetta",
              "kuerzel": "L7",
              "label": "Vendetta",
              "stufe": 7,
              "kosten": 3,
              "text": "A cut at 30 %, then they bleed (not machines).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "omerta",
              "kuerzel": "L9",
              "label": "Omertà",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: crit ×2.5 (×3.5 with a sure crit), +25 % per condition, up to 4.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "W",
          "name": "Marksman",
          "attribut": "perception",
          "attribut_label": "Perception",
          "skills": [
            {
              "id": "point_de_mire",
              "kuerzel": "W3",
              "label": "Point de Mire",
              "stufe": 3,
              "kosten": 2,
              "text": "They are exhausted for 3 rounds (below Perception 4: until your next turn).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "bonaccia",
              "kuerzel": "W5",
              "label": "Bonaccia",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: catch a strong one completely and strike back, halve a weak one and strike back at half strength (below Perception 4: only halved).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "phare",
              "kuerzel": "W7",
              "label": "Phare",
              "stufe": 7,
              "kosten": 3,
              "text": "Against a strong special attack: blinds them and they skip 1 round (2 if charged with current); below Perception 4 only at 15 % per point.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "pluie_d_etoiles",
              "kuerzel": "W9",
              "label": "Pluie d'Étoiles",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: 3 hits at 85 % (full damage against flyers).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "M",
          "name": "Berserker",
          "attribut": "courage",
          "attribut_label": "Courage",
          "skills": [
            {
              "id": "scirocco",
              "kuerzel": "M3",
              "label": "Scirocco",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage and one burn stack, but afterwards you are exposed.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "retour",
              "kuerzel": "M5",
              "label": "Retour de Flamme",
              "stufe": 5,
              "kosten": 2,
              "text": "Charges your weapon: their next attack is met with a counter. Parry it for ×1.5 and a burn stack (×2 against a strong special attack), miss it for ×0.5.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "furia",
              "kuerzel": "M7",
              "label": "Furia",
              "stufe": 7,
              "kosten": 3,
              "text": "One hit right away, then 2 rounds at ×1.3, and every hit adds a burn stack. You catch fire yourself and cannot defend.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "vulcano",
              "kuerzel": "M9",
              "label": "Vulcano",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: one blow per burn stack on the enemy at 60 %, ignores protection and uses up every stack. You skip 1 round afterwards.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        }
      ],
      "hinweis": "The Smuggler path comes into its own with its finisher, Omertà."
    },
    "10:doppio_gioco,mistral,omerta,point_de_mire,sotto_voce,vendetta": {
      "level": 10,
      "level_max": 10,
      "xp": 0,
      "xp_next": 600,
      "skillpunkte": 0,
      "skillpunkte_gesamt": 6,
      "skillpunkte_plan": [
        {
          "level": 3,
          "punkte": 1
        },
        {
          "level": 5,
          "punkte": 1
        },
        {
          "level": 7,
          "punkte": 1
        },
        {
          "level": 9,
          "punkte": 1
        },
        {
          "level": 10,
          "punkte": 2
        }
      ],
      "hauptpfad": "Smuggler",
      "hauptpfad_info": {
        "id": "L",
        "name": "Smuggler",
        "summary": "Growing path attribute: Cunning.",
        "attribute_label": "Cunning",
        "traits": [
          "Cunning grows with this path."
        ]
      },
      "hauptpfad_prioritaet": [
        "Berserker",
        "Fighter",
        "Smuggler",
        "Marksman"
      ],
      "pfade": [
        {
          "id": "K",
          "name": "Fighter",
          "attribut": "strength",
          "attribut_label": "Strength",
          "skills": [
            {
              "id": "mistral",
              "kuerzel": "K3",
              "label": "Mistral",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage, and the enemy is shaken for 2 rounds (no protection).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "ressac",
              "kuerzel": "K5",
              "label": "Ressac",
              "stufe": 5,
              "kosten": 3,
              "text": "Answer to their special attack: a counter (×2 against a wet enemy); against a strong one they are also weakened.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "libeccio",
              "kuerzel": "K7",
              "label": "Libeccio",
              "stufe": 7,
              "kosten": 2,
              "text": "For 2 rounds you take half damage, and every perfect parry shakes them.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "lame_de_fond",
              "kuerzel": "K9",
              "label": "Lame de Fond",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: ×2, against a shaken one ×3.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "L",
          "name": "Smuggler",
          "attribut": "cunning",
          "attribut_label": "Cunning",
          "skills": [
            {
              "id": "doppio_gioco",
              "kuerzel": "L3",
              "label": "Doppio Gioco",
              "stufe": 3,
              "kosten": 3,
              "text": "Two cuts at 70 % each.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "sotto_voce",
              "kuerzel": "L5",
              "label": "Sotto Voce",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: your next attack is a sure crit; against a strong one their hit is also halved.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "vendetta",
              "kuerzel": "L7",
              "label": "Vendetta",
              "stufe": 7,
              "kosten": 3,
              "text": "A cut at 30 %, then they bleed (not machines).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "omerta",
              "kuerzel": "L9",
              "label": "Omertà",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: crit ×2.5 (×3.5 with a sure crit), +25 % per condition, up to 4.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "W",
          "name": "Marksman",
          "attribut": "perception",
          "attribut_label": "Perception",
          "skills": [
            {
              "id": "point_de_mire",
              "kuerzel": "W3",
              "label": "Point de Mire",
              "stufe": 3,
              "kosten": 2,
              "text": "They are exhausted for 3 rounds (below Perception 4: until your next turn).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "bonaccia",
              "kuerzel": "W5",
              "label": "Bonaccia",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: catch a strong one completely and strike back, halve a weak one and strike back at half strength (below Perception 4: only halved).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "phare",
              "kuerzel": "W7",
              "label": "Phare",
              "stufe": 7,
              "kosten": 3,
              "text": "Against a strong special attack: blinds them and they skip 1 round (2 if charged with current); below Perception 4 only at 15 % per point.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "pluie_d_etoiles",
              "kuerzel": "W9",
              "label": "Pluie d'Étoiles",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: 3 hits at 85 % (full damage against flyers).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "M",
          "name": "Berserker",
          "attribut": "courage",
          "attribut_label": "Courage",
          "skills": [
            {
              "id": "scirocco",
              "kuerzel": "M3",
              "label": "Scirocco",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage and one burn stack, but afterwards you are exposed.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "retour",
              "kuerzel": "M5",
              "label": "Retour de Flamme",
              "stufe": 5,
              "kosten": 2,
              "text": "Charges your weapon: their next attack is met with a counter. Parry it for ×1.5 and a burn stack (×2 against a strong special attack), miss it for ×0.5.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "furia",
              "kuerzel": "M7",
              "label": "Furia",
              "stufe": 7,
              "kosten": 3,
              "text": "One hit right away, then 2 rounds at ×1.3, and every hit adds a burn stack. You catch fire yourself and cannot defend.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "vulcano",
              "kuerzel": "M9",
              "label": "Vulcano",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: one blow per burn stack on the enemy at 60 %, ignores protection and uses up every stack. You skip 1 round afterwards.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        }
      ],
      "hinweis": null
    },
    "10:doppio_gioco,mistral,omerta,scirocco,sotto_voce,vendetta": {
      "level": 10,
      "level_max": 10,
      "xp": 0,
      "xp_next": 600,
      "skillpunkte": 0,
      "skillpunkte_gesamt": 6,
      "skillpunkte_plan": [
        {
          "level": 3,
          "punkte": 1
        },
        {
          "level": 5,
          "punkte": 1
        },
        {
          "level": 7,
          "punkte": 1
        },
        {
          "level": 9,
          "punkte": 1
        },
        {
          "level": 10,
          "punkte": 2
        }
      ],
      "hauptpfad": "Smuggler",
      "hauptpfad_info": {
        "id": "L",
        "name": "Smuggler",
        "summary": "Growing path attribute: Cunning.",
        "attribute_label": "Cunning",
        "traits": [
          "Cunning grows with this path."
        ]
      },
      "hauptpfad_prioritaet": [
        "Berserker",
        "Fighter",
        "Smuggler",
        "Marksman"
      ],
      "pfade": [
        {
          "id": "K",
          "name": "Fighter",
          "attribut": "strength",
          "attribut_label": "Strength",
          "skills": [
            {
              "id": "mistral",
              "kuerzel": "K3",
              "label": "Mistral",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage, and the enemy is shaken for 2 rounds (no protection).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "ressac",
              "kuerzel": "K5",
              "label": "Ressac",
              "stufe": 5,
              "kosten": 3,
              "text": "Answer to their special attack: a counter (×2 against a wet enemy); against a strong one they are also weakened.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "libeccio",
              "kuerzel": "K7",
              "label": "Libeccio",
              "stufe": 7,
              "kosten": 2,
              "text": "For 2 rounds you take half damage, and every perfect parry shakes them.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "lame_de_fond",
              "kuerzel": "K9",
              "label": "Lame de Fond",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: ×2, against a shaken one ×3.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "L",
          "name": "Smuggler",
          "attribut": "cunning",
          "attribut_label": "Cunning",
          "skills": [
            {
              "id": "doppio_gioco",
              "kuerzel": "L3",
              "label": "Doppio Gioco",
              "stufe": 3,
              "kosten": 3,
              "text": "Two cuts at 70 % each.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "sotto_voce",
              "kuerzel": "L5",
              "label": "Sotto Voce",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: your next attack is a sure crit; against a strong one their hit is also halved.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "vendetta",
              "kuerzel": "L7",
              "label": "Vendetta",
              "stufe": 7,
              "kosten": 3,
              "text": "A cut at 30 %, then they bleed (not machines).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "omerta",
              "kuerzel": "L9",
              "label": "Omertà",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: crit ×2.5 (×3.5 with a sure crit), +25 % per condition, up to 4.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "W",
          "name": "Marksman",
          "attribut": "perception",
          "attribut_label": "Perception",
          "skills": [
            {
              "id": "point_de_mire",
              "kuerzel": "W3",
              "label": "Point de Mire",
              "stufe": 3,
              "kosten": 2,
              "text": "They are exhausted for 3 rounds (below Perception 4: until your next turn).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "bonaccia",
              "kuerzel": "W5",
              "label": "Bonaccia",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: catch a strong one completely and strike back, halve a weak one and strike back at half strength (below Perception 4: only halved).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "phare",
              "kuerzel": "W7",
              "label": "Phare",
              "stufe": 7,
              "kosten": 3,
              "text": "Against a strong special attack: blinds them and they skip 1 round (2 if charged with current); below Perception 4 only at 15 % per point.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "pluie_d_etoiles",
              "kuerzel": "W9",
              "label": "Pluie d'Étoiles",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: 3 hits at 85 % (full damage against flyers).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "M",
          "name": "Berserker",
          "attribut": "courage",
          "attribut_label": "Courage",
          "skills": [
            {
              "id": "scirocco",
              "kuerzel": "M3",
              "label": "Scirocco",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage and one burn stack, but afterwards you are exposed.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "retour",
              "kuerzel": "M5",
              "label": "Retour de Flamme",
              "stufe": 5,
              "kosten": 2,
              "text": "Charges your weapon: their next attack is met with a counter. Parry it for ×1.5 and a burn stack (×2 against a strong special attack), miss it for ×0.5.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "furia",
              "kuerzel": "M7",
              "label": "Furia",
              "stufe": 7,
              "kosten": 3,
              "text": "One hit right away, then 2 rounds at ×1.3, and every hit adds a burn stack. You catch fire yourself and cannot defend.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "vulcano",
              "kuerzel": "M9",
              "label": "Vulcano",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: one blow per burn stack on the enemy at 60 %, ignores protection and uses up every stack. You skip 1 round afterwards.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        }
      ],
      "hinweis": null
    },
    "10:bonaccia,doppio_gioco,mistral,point_de_mire,sotto_voce,vendetta": {
      "level": 10,
      "level_max": 10,
      "xp": 0,
      "xp_next": 600,
      "skillpunkte": 0,
      "skillpunkte_gesamt": 6,
      "skillpunkte_plan": [
        {
          "level": 3,
          "punkte": 1
        },
        {
          "level": 5,
          "punkte": 1
        },
        {
          "level": 7,
          "punkte": 1
        },
        {
          "level": 9,
          "punkte": 1
        },
        {
          "level": 10,
          "punkte": 2
        }
      ],
      "hauptpfad": "Smuggler",
      "hauptpfad_info": {
        "id": "L",
        "name": "Smuggler",
        "summary": "Growing path attribute: Cunning.",
        "attribute_label": "Cunning",
        "traits": [
          "Cunning grows with this path."
        ]
      },
      "hauptpfad_prioritaet": [
        "Berserker",
        "Fighter",
        "Smuggler",
        "Marksman"
      ],
      "pfade": [
        {
          "id": "K",
          "name": "Fighter",
          "attribut": "strength",
          "attribut_label": "Strength",
          "skills": [
            {
              "id": "mistral",
              "kuerzel": "K3",
              "label": "Mistral",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage, and the enemy is shaken for 2 rounds (no protection).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "ressac",
              "kuerzel": "K5",
              "label": "Ressac",
              "stufe": 5,
              "kosten": 3,
              "text": "Answer to their special attack: a counter (×2 against a wet enemy); against a strong one they are also weakened.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "libeccio",
              "kuerzel": "K7",
              "label": "Libeccio",
              "stufe": 7,
              "kosten": 2,
              "text": "For 2 rounds you take half damage, and every perfect parry shakes them.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "lame_de_fond",
              "kuerzel": "K9",
              "label": "Lame de Fond",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: ×2, against a shaken one ×3.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "L",
          "name": "Smuggler",
          "attribut": "cunning",
          "attribut_label": "Cunning",
          "skills": [
            {
              "id": "doppio_gioco",
              "kuerzel": "L3",
              "label": "Doppio Gioco",
              "stufe": 3,
              "kosten": 3,
              "text": "Two cuts at 70 % each.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "sotto_voce",
              "kuerzel": "L5",
              "label": "Sotto Voce",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: your next attack is a sure crit; against a strong one their hit is also halved.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "vendetta",
              "kuerzel": "L7",
              "label": "Vendetta",
              "stufe": 7,
              "kosten": 3,
              "text": "A cut at 30 %, then they bleed (not machines).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "omerta",
              "kuerzel": "L9",
              "label": "Omertà",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: crit ×2.5 (×3.5 with a sure crit), +25 % per condition, up to 4.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "W",
          "name": "Marksman",
          "attribut": "perception",
          "attribut_label": "Perception",
          "skills": [
            {
              "id": "point_de_mire",
              "kuerzel": "W3",
              "label": "Point de Mire",
              "stufe": 3,
              "kosten": 2,
              "text": "They are exhausted for 3 rounds (below Perception 4: until your next turn).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "bonaccia",
              "kuerzel": "W5",
              "label": "Bonaccia",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: catch a strong one completely and strike back, halve a weak one and strike back at half strength (below Perception 4: only halved).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "phare",
              "kuerzel": "W7",
              "label": "Phare",
              "stufe": 7,
              "kosten": 3,
              "text": "Against a strong special attack: blinds them and they skip 1 round (2 if charged with current); below Perception 4 only at 15 % per point.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "pluie_d_etoiles",
              "kuerzel": "W9",
              "label": "Pluie d'Étoiles",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: 3 hits at 85 % (full damage against flyers).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "M",
          "name": "Berserker",
          "attribut": "courage",
          "attribut_label": "Courage",
          "skills": [
            {
              "id": "scirocco",
              "kuerzel": "M3",
              "label": "Scirocco",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage and one burn stack, but afterwards you are exposed.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "retour",
              "kuerzel": "M5",
              "label": "Retour de Flamme",
              "stufe": 5,
              "kosten": 2,
              "text": "Charges your weapon: their next attack is met with a counter. Parry it for ×1.5 and a burn stack (×2 against a strong special attack), miss it for ×0.5.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "furia",
              "kuerzel": "M7",
              "label": "Furia",
              "stufe": 7,
              "kosten": 3,
              "text": "One hit right away, then 2 rounds at ×1.3, and every hit adds a burn stack. You catch fire yourself and cannot defend.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "vulcano",
              "kuerzel": "M9",
              "label": "Vulcano",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: one blow per burn stack on the enemy at 60 %, ignores protection and uses up every stack. You skip 1 round afterwards.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        }
      ],
      "hinweis": "The Smuggler path comes into its own with its finisher, Omertà."
    },
    "10:doppio_gioco,mistral,point_de_mire,scirocco,sotto_voce,vendetta": {
      "level": 10,
      "level_max": 10,
      "xp": 0,
      "xp_next": 600,
      "skillpunkte": 0,
      "skillpunkte_gesamt": 6,
      "skillpunkte_plan": [
        {
          "level": 3,
          "punkte": 1
        },
        {
          "level": 5,
          "punkte": 1
        },
        {
          "level": 7,
          "punkte": 1
        },
        {
          "level": 9,
          "punkte": 1
        },
        {
          "level": 10,
          "punkte": 2
        }
      ],
      "hauptpfad": "Smuggler",
      "hauptpfad_info": {
        "id": "L",
        "name": "Smuggler",
        "summary": "Growing path attribute: Cunning.",
        "attribute_label": "Cunning",
        "traits": [
          "Cunning grows with this path."
        ]
      },
      "hauptpfad_prioritaet": [
        "Berserker",
        "Fighter",
        "Smuggler",
        "Marksman"
      ],
      "pfade": [
        {
          "id": "K",
          "name": "Fighter",
          "attribut": "strength",
          "attribut_label": "Strength",
          "skills": [
            {
              "id": "mistral",
              "kuerzel": "K3",
              "label": "Mistral",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage, and the enemy is shaken for 2 rounds (no protection).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "ressac",
              "kuerzel": "K5",
              "label": "Ressac",
              "stufe": 5,
              "kosten": 3,
              "text": "Answer to their special attack: a counter (×2 against a wet enemy); against a strong one they are also weakened.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "libeccio",
              "kuerzel": "K7",
              "label": "Libeccio",
              "stufe": 7,
              "kosten": 2,
              "text": "For 2 rounds you take half damage, and every perfect parry shakes them.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "lame_de_fond",
              "kuerzel": "K9",
              "label": "Lame de Fond",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: ×2, against a shaken one ×3.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "L",
          "name": "Smuggler",
          "attribut": "cunning",
          "attribut_label": "Cunning",
          "skills": [
            {
              "id": "doppio_gioco",
              "kuerzel": "L3",
              "label": "Doppio Gioco",
              "stufe": 3,
              "kosten": 3,
              "text": "Two cuts at 70 % each.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "sotto_voce",
              "kuerzel": "L5",
              "label": "Sotto Voce",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: your next attack is a sure crit; against a strong one their hit is also halved.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "vendetta",
              "kuerzel": "L7",
              "label": "Vendetta",
              "stufe": 7,
              "kosten": 3,
              "text": "A cut at 30 %, then they bleed (not machines).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "omerta",
              "kuerzel": "L9",
              "label": "Omertà",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: crit ×2.5 (×3.5 with a sure crit), +25 % per condition, up to 4.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "W",
          "name": "Marksman",
          "attribut": "perception",
          "attribut_label": "Perception",
          "skills": [
            {
              "id": "point_de_mire",
              "kuerzel": "W3",
              "label": "Point de Mire",
              "stufe": 3,
              "kosten": 2,
              "text": "They are exhausted for 3 rounds (below Perception 4: until your next turn).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "bonaccia",
              "kuerzel": "W5",
              "label": "Bonaccia",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: catch a strong one completely and strike back, halve a weak one and strike back at half strength (below Perception 4: only halved).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "phare",
              "kuerzel": "W7",
              "label": "Phare",
              "stufe": 7,
              "kosten": 3,
              "text": "Against a strong special attack: blinds them and they skip 1 round (2 if charged with current); below Perception 4 only at 15 % per point.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "pluie_d_etoiles",
              "kuerzel": "W9",
              "label": "Pluie d'Étoiles",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: 3 hits at 85 % (full damage against flyers).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "M",
          "name": "Berserker",
          "attribut": "courage",
          "attribut_label": "Courage",
          "skills": [
            {
              "id": "scirocco",
              "kuerzel": "M3",
              "label": "Scirocco",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage and one burn stack, but afterwards you are exposed.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "retour",
              "kuerzel": "M5",
              "label": "Retour de Flamme",
              "stufe": 5,
              "kosten": 2,
              "text": "Charges your weapon: their next attack is met with a counter. Parry it for ×1.5 and a burn stack (×2 against a strong special attack), miss it for ×0.5.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "furia",
              "kuerzel": "M7",
              "label": "Furia",
              "stufe": 7,
              "kosten": 3,
              "text": "One hit right away, then 2 rounds at ×1.3, and every hit adds a burn stack. You catch fire yourself and cannot defend.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "vulcano",
              "kuerzel": "M9",
              "label": "Vulcano",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: one blow per burn stack on the enemy at 60 %, ignores protection and uses up every stack. You skip 1 round afterwards.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        }
      ],
      "hinweis": "The Smuggler path comes into its own with its finisher, Omertà."
    },
    "10:doppio_gioco,mistral,retour,scirocco,sotto_voce,vendetta": {
      "level": 10,
      "level_max": 10,
      "xp": 0,
      "xp_next": 600,
      "skillpunkte": 0,
      "skillpunkte_gesamt": 6,
      "skillpunkte_plan": [
        {
          "level": 3,
          "punkte": 1
        },
        {
          "level": 5,
          "punkte": 1
        },
        {
          "level": 7,
          "punkte": 1
        },
        {
          "level": 9,
          "punkte": 1
        },
        {
          "level": 10,
          "punkte": 2
        }
      ],
      "hauptpfad": "Smuggler",
      "hauptpfad_info": {
        "id": "L",
        "name": "Smuggler",
        "summary": "Growing path attribute: Cunning.",
        "attribute_label": "Cunning",
        "traits": [
          "Cunning grows with this path."
        ]
      },
      "hauptpfad_prioritaet": [
        "Berserker",
        "Fighter",
        "Smuggler",
        "Marksman"
      ],
      "pfade": [
        {
          "id": "K",
          "name": "Fighter",
          "attribut": "strength",
          "attribut_label": "Strength",
          "skills": [
            {
              "id": "mistral",
              "kuerzel": "K3",
              "label": "Mistral",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage, and the enemy is shaken for 2 rounds (no protection).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "ressac",
              "kuerzel": "K5",
              "label": "Ressac",
              "stufe": 5,
              "kosten": 3,
              "text": "Answer to their special attack: a counter (×2 against a wet enemy); against a strong one they are also weakened.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "libeccio",
              "kuerzel": "K7",
              "label": "Libeccio",
              "stufe": 7,
              "kosten": 2,
              "text": "For 2 rounds you take half damage, and every perfect parry shakes them.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "lame_de_fond",
              "kuerzel": "K9",
              "label": "Lame de Fond",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: ×2, against a shaken one ×3.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "L",
          "name": "Smuggler",
          "attribut": "cunning",
          "attribut_label": "Cunning",
          "skills": [
            {
              "id": "doppio_gioco",
              "kuerzel": "L3",
              "label": "Doppio Gioco",
              "stufe": 3,
              "kosten": 3,
              "text": "Two cuts at 70 % each.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "sotto_voce",
              "kuerzel": "L5",
              "label": "Sotto Voce",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: your next attack is a sure crit; against a strong one their hit is also halved.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "vendetta",
              "kuerzel": "L7",
              "label": "Vendetta",
              "stufe": 7,
              "kosten": 3,
              "text": "A cut at 30 %, then they bleed (not machines).",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "omerta",
              "kuerzel": "L9",
              "label": "Omertà",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher against an exhausted enemy: crit ×2.5 (×3.5 with a sure crit), +25 % per condition, up to 4.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "W",
          "name": "Marksman",
          "attribut": "perception",
          "attribut_label": "Perception",
          "skills": [
            {
              "id": "point_de_mire",
              "kuerzel": "W3",
              "label": "Point de Mire",
              "stufe": 3,
              "kosten": 2,
              "text": "They are exhausted for 3 rounds (below Perception 4: until your next turn).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "bonaccia",
              "kuerzel": "W5",
              "label": "Bonaccia",
              "stufe": 5,
              "kosten": 2,
              "text": "Answer to their special attack: catch a strong one completely and strike back, halve a weak one and strike back at half strength (below Perception 4: only halved).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "phare",
              "kuerzel": "W7",
              "label": "Phare",
              "stufe": 7,
              "kosten": 3,
              "text": "Against a strong special attack: blinds them and they skip 1 round (2 if charged with current); below Perception 4 only at 15 % per point.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "pluie_d_etoiles",
              "kuerzel": "W9",
              "label": "Pluie d'Étoiles",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: 3 hits at 85 % (full damage against flyers).",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        },
        {
          "id": "M",
          "name": "Berserker",
          "attribut": "courage",
          "attribut_label": "Courage",
          "skills": [
            {
              "id": "scirocco",
              "kuerzel": "M3",
              "label": "Scirocco",
              "stufe": 3,
              "kosten": 3,
              "text": "+4 damage and one burn stack, but afterwards you are exposed.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "retour",
              "kuerzel": "M5",
              "label": "Retour de Flamme",
              "stufe": 5,
              "kosten": 2,
              "text": "Charges your weapon: their next attack is met with a counter. Parry it for ×1.5 and a burn stack (×2 against a strong special attack), miss it for ×0.5.",
              "gelernt": true,
              "grund": null,
              "lernfolgen": null
            },
            {
              "id": "furia",
              "kuerzel": "M7",
              "label": "Furia",
              "stufe": 7,
              "kosten": 3,
              "text": "One hit right away, then 2 rounds at ×1.3, and every hit adds a burn stack. You catch fire yourself and cannot defend.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            },
            {
              "id": "vulcano",
              "kuerzel": "M9",
              "label": "Vulcano",
              "stufe": 9,
              "kosten": 4,
              "text": "Finisher: one blow per burn stack on the enemy at 60 %, ignores protection and uses up every stack. You skip 1 round afterwards.",
              "gelernt": false,
              "grund": "No free skill point.",
              "lernfolgen": null
            }
          ]
        }
      ],
      "hinweis": "The Smuggler path comes into its own with its finisher, Omertà."
    }
  }
};
