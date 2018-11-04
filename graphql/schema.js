const schema = `

  type User {
    id: ID!
    name: String!
    created_at: String!
    topics: [Topic!]
	}

  type Topic {
    id: ID!
    title: String!
    user_id: ID!
    user: User!
    links: [Link!]
	}

  type Link {
    id: ID!
    title: String!
    url: String!
    topic_id: ID!
    topic: Topic!
    tags: [Tag!]
	}

  type Tag {
    id: ID!
    title: String!
	}

  type Query {
    topic(id: ID!): Topic
    topics: [Topic!]
    user(id: ID!): User
    users: [User!]
    link(id: ID!): Link
    links: [Link!]
    tag(id: ID!): Tag
    tags: [Tag!]
	}
`;

module.exports = schema;
