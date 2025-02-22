-- Tabela User
CREATE TABLE "User" (
    id SERIAL PRIMARY KEY,
    avatar_url VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    nome VARCHAR(255),
    bio TEXT,
    nickname VARCHAR(255) UNIQUE,
    phone VARCHAR(20),
    password VARCHAR(255),
    social_networks JSONB, -- Usando JSONB para flexibilidade nas redes sociais
    role VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Tabela Hotwheels
CREATE TABLE Hotwheels (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(255),
    image_url VARCHAR(255),
    collector_number VARCHAR(50),
    series_number VARCHAR(50),
    release_year INTEGER,
    series VARCHAR(255),
    color VARCHAR(50),
    tampo VARCHAR(255),
    wheel_type VARCHAR(100),
    base_type VARCHAR(100),
    base_color VARCHAR(50),
    window_color VARCHAR(50),
    interior_color VARCHAR(50),
    toy_number VARCHAR(50),
    assortment_number VARCHAR(50),
    scale VARCHAR(50),
    country VARCHAR(100),
    base_codes VARCHAR(255),
    case_number VARCHAR(50),
    notes TEXT,
    treasure_hunt_year INTEGER,
    super_treasure_hunt_year INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Tabela user_hotwheels (Relacionamento entre User e Hotwheels)
CREATE TABLE user_hotwheels (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "User"(id) ON DELETE CASCADE,
    hotwheels_id INTEGER NOT NULL REFERENCES Hotwheels(id) ON DELETE CASCADE,
    modality VARCHAR(50), -- Ex: 'collection', 'sale', 'trade'
    favorite BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Tabela collections (Coleções de usuários)
CREATE TABLE collections (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "User"(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    display_order INTEGER,
    CONSTRAINT unique_user_display_order UNIQUE (user_id, display_order) -- Garante a unicidade da ordem por usuário
);

-- Tabela collection_items (Itens dentro de uma coleção)
CREATE TABLE collection_items (
    id SERIAL PRIMARY KEY,
    collection_id INTEGER NOT NULL REFERENCES collections(id) ON DELETE CASCADE,
    hotwheel_id INTEGER NOT NULL REFERENCES Hotwheels(id) ON DELETE CASCADE,
    position INTEGER -- Posição do item na coleção, pode ser null ou ter lógica de ordenação
);

-- Tabela Wishlist (Lista de desejos do usuário)
CREATE TABLE Wishlist (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "User"(id) ON DELETE CASCADE,
    hotwheels_id INTEGER NOT NULL REFERENCES Hotwheels(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Tabela user_hotwheels_sale (Detalhes de venda de um user_hotwheels)
CREATE TABLE user_hotwheels_sale (
    id SERIAL PRIMARY KEY,
    user_hotwheels_id INTEGER NOT NULL REFERENCES user_hotwheels(id) ON DELETE CASCADE,
    price DECIMAL(10, 2) -- Preço de venda
);