module.exports = `
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
  type Mutation {
    createTopic(title: String, user_id: ID!): Topic!
  }
`;

/*

updateTopic(id: ID!, title: String): Topic
deleteTopic(id: ID!): Int!
createLink(title: String!, url: String!, topicId: ID!): Link
updateLink(id: ID!, title: String!, url: String!): Link
deleteLink(id: ID!): Int!
createLink
createTag
topic.addLink
topic.removeLink
topic.link.addTag
topic.link.removeTag
*/
