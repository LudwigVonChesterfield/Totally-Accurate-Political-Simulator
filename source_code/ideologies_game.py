"""
!!!DISCLAIMER!!!
ALL INFORMATION CONTAINED IN THIS FILE HAS NOTHING TO DO WITH REAL LIFE.
ALL CHARACTERS DESCRIBED HERE ARE FICTIONARY.
ANY AND ALL SIMILARITIES ARE COMPLETELY COINCIDENTAL.
"""

IDEOLOGIES_CLASSIFICATION = {
    # """Centrists""".
    "Centrism":
    {"Axis":  # Technically a list of all axis. Albeit all of them are zero.
        {"Liberty-Authority": 0,
         "Pacifism-Militarism": 0,
         "Materialism-Spiritualism": 0,
         "Individualism-Collectivism": 0,
         "Reformism-Revolutionism": 0,
         "Industrialism-Primitivism": 0
        },
    "Foreground": "Silver",
    "Background": "DarkSlateGray"
    },

    # Communists.
    "Communism":
    {"Axis":
        {"Liberty-Authority": -100,
         "Pacifism-Militarism": 0,
         "Materialism-Spiritualism": 0,
         "Individualism-Collectivism": -100,
         "Reformism-Revolutionism": 0,
         "Industrialism-Primitivism": 100
        },
    "Foreground": "Red",
    "Background": "Red"
    },

    "Anarcho-communism":
    {"Axis":
        {"Liberty-Authority": 100,
         "Pacifism-Militarism": 0,
         "Materialism-Spiritualism": 0,
         "Individualism-Collectivism": -100,
         "Reformism-Revolutionism": 0,
         "Industrialism-Primitivism": 100
        },
    "Foreground": "Red",
    "Background": "Navy"
    },

    "Trotskyism":
    {"Axis":
        {"Liberty-Authority": -100,
         "Pacifism-Militarism": 0,
         "Materialism-Spiritualism": 0,
         "Individualism-Collectivism": -100,
         "Reformism-Revolutionism": -100,
         "Industrialism-Primitivism": 100
        },
    "Foreground": "White",
    "Background": "FireBrick"
    },

    "Anarcho-trotskyism":
    {"Axis":
        {"Liberty-Authority": 100,
         "Pacifism-Militarism": 0,
         "Materialism-Spiritualism": 0,
         "Individualism-Collectivism": -100,
         "Reformism-Revolutionism": -100,
         "Industrialism-Primitivism": 100
        },
    "Foreground": "FireBrick",
    "Background": "Navy",
    },

    "Posadism":
    {"Axis":
        {"Liberty-Authority": -100,
         "Pacifism-Militarism": -100,
         "Materialism-Spiritualism": 0,
         "Individualism-Collectivism": -100,
         "Reformism-Revolutionism": -100,
         "Industrialism-Primitivism": 100
        },
    "Foreground": "Yellow",
    "Background": "FireBrick"
    },

    "Anarcho-posadism":
    {"Axis":
        {"Liberty-Authority": 100,
         "Pacifism-Militarism": -100,
         "Materialism-Spiritualism": 0,
         "Individualism-Collectivism": -100,
         "Reformism-Revolutionism": -100,
         "Industrialism-Primitivism": 100
        },
    "Foreground": "FireBrick",
    "Background": "Navy"
    },

    # Capitalists.
    "Capitalism":
    {"Axis":
        {"Liberty-Authority": 0,
         "Pacifism-Militarism": 0,
         "Materialism-Spiritualism": 100,
         "Individualism-Collectivism": 100,
         "Reformism-Revolutionism": 0,
         "Industrialism-Primitivism": 100
        },
    "Foreground": "Yellow",
    "Background": "Yellow"
    },

    "Liberal capitalism":
    {"Axis":
        {"Liberty-Authority": 50,
         "Pacifism-Militarism": 0,
         "Materialism-Spiritualism": 100,
         "Individualism-Collectivism": 100,
         "Reformism-Revolutionism": 0,
         "Industrialism-Primitivism": 100
        },
    "Foreground": "Yellow",
    "Background": "LightSlateGrey"
    },

    "Anarcho-capitalism":
    {"Axis":
        {"Liberty-Authority": 100,
         "Pacifism-Militarism": 0,
         "Materialism-Spiritualism": 100,
         "Individualism-Collectivism": 100,
         "Reformism-Revolutionism": 0,
         "Industrialism-Primitivism": 100
        },
    "Foreground": "Yellow",
    "Background": "Navy"
    },

    # Fascists.
    "Fascism":
    {"Axis":
        {"Liberty-Authority": -100,
         "Pacifism-Militarism": -100,
         "Materialism-Spiritualism": 0,
         "Individualism-Collectivism": -100,
         "Reformism-Revolutionism": 0,
         "Industrialism-Primitivism": 0,
        },
    "Foreground": "Sienna",
    "Background": "Sienna"
    },

    "Anarcho-fascism":
    {"Axis":
        {"Liberty-Authority": 100,
         "Pacifism-Militarism": -100,
         "Materialism-Spiritualism": 0,
         "Individualism-Collectivism": -100,
         "Reformism-Revolutionism": 0,
         "Industrialism-Primitivism": 0,
        },
    "Foreground": "Sienna",
    "Background": "Navy"
    },

    "Strasserism":
    {"Axis":
        {"Liberty-Authority": -100,
         "Pacifism-Militarism": -100,
         "Materialism-Spiritualism": 0,
         "Individualism-Collectivism": -100,
         "Reformism-Revolutionism": 0,
         "Industrialism-Primitivism": 100,
        },
    "Foreground": "Sienna",
    "Background": "Yellow"
    },

   "Ecofascism":
    {"Axis":
        {"Liberty-Authority": -100,
         "Pacifism-Militarism": -100,
         "Materialism-Spiritualism": 0,
         "Individualism-Collectivism": -100,
         "Reformism-Revolutionism": 0,
         "Industrialism-Primitivism": -100,
        },
    "Foreground": "Sienna",
    "Background": "Green"
    },

    "Techno-fascism":
    {"Axis":
        {"Liberty-Authority": -100,
         "Pacifism-Militarism": -100,
         "Materialism-Spiritualism": 100,
         "Individualism-Collectivism": -100,
         "Reformism-Revolutionism": 0,
         "Industrialism-Primitivism": 0,
        },
    "Foreground": "Sienna",
    "Background": "Blue"
    },

   "Esoteric fascism":
    {"Axis":
        {"Liberty-Authority": -100,
         "Pacifism-Militarism": -100,
         "Materialism-Spiritualism": -100,
         "Individualism-Collectivism": -100,
         "Reformism-Revolutionism": 0,
         "Industrialism-Primitivism": 0,
        },
    "Foreground": "Sienna",
    "Background": "Purple"
    },

    # Syndicalists.
    "Syndicalism":
    {"Axis":
        {"Liberty-Authority": 0,
         "Pacifism-Militarism": 0,
         "Materialism-Spiritualism": 0,
         "Individualism-Collectivism": -100,
         "Reformism-Revolutionism": -100,
         "Industrialism-Primitivism": 100
        },
    "Foreground": "FireBrick",
    "Background": "Navy"  # Look at Anarcho-syndicalism. Do you see the joke?
    },

    "Anarcho-syndicalism":
    {"Axis":
        {"Liberty-Authority": 100,
         "Pacifism-Militarism": 0,
         "Materialism-Spiritualism": 0,
         "Individualism-Collectivism": -100,
         "Reformism-Revolutionism": -100,
         "Industrialism-Primitivism": 100
        },
    "Foreground": "FireBrick",
    "Background": "Navy"
    },

   "Fascist syndicalism":
    {"Axis":
        {"Liberty-Authority": -100,
         "Pacifism-Militarism": -100,
         "Materialism-Spiritualism": 0,
         "Individualism-Collectivism": -100,
         "Reformism-Revolutionism": -100,
         "Industrialism-Primitivism": 100
        },
    "Foreground": "FireBrick",
    "Background": "Sienna"
    },

    # Government enthusiasts.
    "Statism":
    {"Axis":
        {"Liberty-Authority": -100,
         "Pacifism-Militarism": 0,
         "Materialism-Spiritualism": 0,
         "Individualism-Collectivism": -100,
         "Reformism-Revolutionism": 0,
         "Industrialism-Primitivism": 0
        },
    "Foreground": "Red",
    "Background": "Blue"
    },

    "Minarchism":
    {"Axis":
        {"Liberty-Authority": -50,
         "Pacifism-Militarism": 0,
         "Materialism-Spiritualism": 0,
         "Individualism-Collectivism": -50,
         "Reformism-Revolutionism": 0,
         "Industrialism-Primitivism": 0
        },
    "Foreground": "Yellow",
    "Background": "Blue"
    },

    "Social democracy":
    {"Axis":
        {"Liberty-Authority": -50,
         "Pacifism-Militarism": 50,
         "Materialism-Spiritualism": 0,
         "Individualism-Collectivism": -50,
         "Reformism-Revolutionism": 50,
         "Industrialism-Primitivism": 0
        },
    "Foreground": "Blue",
    "Background": "Yellow"
    },

    # Peaceful protesters.
    "Agorism":
    {"Axis":
        {"Liberty-Authority": 100,
         "Pacifism-Militarism": 100,
         "Materialism-Spiritualism": 0,
         "Individualism-Collectivism": 0,
         "Reformism-Revolutionism": -100,
         "Industrialism-Primitivism": 100
        },
    "Foreground": "Silver",
    "Background": "Navy"
    },

    # "Greens".
    "Green politics":
    {"Axis":
        {"Liberty-Authority": 0,
         "Pacifism-Militarism": 100,
         "Materialism-Spiritualism": 0,
         "Individualism-Collectivism": -100,
         "Reformism-Revolutionism": 0,
         "Industrialism-Primitivism": -50
        },
    "Foreground": "Green",
    "Background": "White"
    },

    "Anarcho-primitivism":
    {"Axis":
        {"Liberty-Authority": 100,
         "Pacifism-Militarism": 0,
         "Materialism-Spiritualism": 0,
         "Individualism-Collectivism": 0,
         "Reformism-Revolutionism": 0,
         "Industrialism-Primitivism": -100
        },
    "Foreground": "Green",
    "Background": "Navy"
    },

    # EGO.
    "Anarcho-individualism":
    {"Axis":
        {"Liberty-Authority": 100,
         "Pacifism-Militarism": 0,
         "Materialism-Spiritualism": 0,
         "Individualism-Collectivism": 100,
         "Reformism-Revolutionism": 0,
         "Industrialism-Primitivism": 0
        },
    "Foreground": "Cyan",
    "Background": "Navy"
    },

    "Meritocracy":
    {"Axis":
        {"Liberty-Authority": -100,
         "Pacifism-Militarism": 0,
         "Materialism-Spiritualism": 0,
         "Individualism-Collectivism": 100,
         "Reformism-Revolutionism": 0,
         "Industrialism-Primitivism": 0
        },
    "Foreground": "Cyan",
    "Background": "Red"
    },

    "Technocracy":
    {"Axis":
        {"Liberty-Authority": -100,
         "Pacifism-Militarism": 0,
         "Materialism-Spiritualism": 100,
         "Individualism-Collectivism": 100,
         "Reformism-Revolutionism": 0,
         "Industrialism-Primitivism": 0
        },
    "Foreground": "Cyan",
    "Background": "Blue"
    },

    # Spiritualists.
    "Theocracy":
    {"Axis":
        {"Liberty-Authority": -100,
         "Pacifism-Militarism": 0,
         "Materialism-Spiritualism": -100,
         "Individualism-Collectivism": 0,
         "Reformism-Revolutionism": 0,
         "Industrialism-Primitivism": 0
        },
    "Foreground": "Purple",
    "Background": "Purple"
    },

    "Liberation theology":
    {"Axis":
        {"Liberty-Authority": -50,
         "Pacifism-Militarism": 50,
         "Materialism-Spiritualism": -100,
         "Individualism-Collectivism": -50,
         "Reformism-Revolutionism": 0,
         "Industrialism-Primitivism": 0
        },
    "Foreground": "Purple",
    "Background": "Red"
    },

    # Radicals vulgaris.
    "Liberalism":
    {"Axis":
        {"Liberty-Authority": 50,
         "Pacifism-Militarism": 0,
         "Materialism-Spiritualism": 0,
         "Individualism-Collectivism": 0,
         "Reformism-Revolutionism": 0,
         "Industrialism-Primitivism": 0
        },
    "Foreground": "LightSlateGrey",
    "Background": "LightSlateGrey"
    },


    # Extremes vulgaris.
    "Anarchism":
    {"Axis":
        {"Liberty-Authority": 100,
         "Pacifism-Militarism": 0,
         "Materialism-Spiritualism": 0,
         "Individualism-Collectivism": 0,
         "Reformism-Revolutionism": 0,
         "Industrialism-Primitivism": 0
        },
    "Foreground": "Navy",
    "Background": "Navy"  # Sadly I use black for background, so Anarchists will have to be "Navy", until a better solution is found...
    },

    "Transhumanism":
    {"Axis":
        {"Liberty-Authority": 0,
         "Pacifism-Militarism": 0,
         "Materialism-Spiritualism": 100,
         "Individualism-Collectivism": 0,
         "Reformism-Revolutionism": 0,
         "Industrialism-Primitivism": 0
        },
    "Foreground": "Blue",
    "Background": "Blue"
    },

    "Conservatism":
    {"Axis":
        {"Liberty-Authority": 0,
         "Pacifism-Militarism": 0,
         "Materialism-Spiritualism": 0,
         "Individualism-Collectivism": 0,
         "Reformism-Revolutionism": 100,
         "Industrialism-Primitivism": 0
        },
    "Foreground": "Dodgerblue",
    "Background": "Dodgerblue"
    },

    "Accelerationism":
    {"Axis":
        {"Liberty-Authority": 0,
         "Pacifism-Militarism": 0,
         "Materialism-Spiritualism": 0,
         "Individualism-Collectivism": 0,
         "Reformism-Revolutionism": -100,
         "Industrialism-Primitivism": 0
        },
    "Foreground": "White",
    "Background": "White"
    },
}
