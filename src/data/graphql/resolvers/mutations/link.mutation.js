const { check, previewLink } = require('lib/helpers');
const config = require('config');

module.exports = {
  createLink: async (
    _,
    { data: { title, url, topic_id, tags } },
    { db, authUser }
  ) => {
    try {
      check.Auth(authUser);
      const topic = await db.topics.findByPk(topic_id);
      if (authUser.id === topic.user_id) {
        
        if( !title ) {
          const linkData = await previewLink(url);
          title = linkData.title;
        }

        return  await db.links.create(
          { title, url, topic_id, tags },
          {
            include: [{ model: db.topics }, { model: db.tags }]
          }
        );
          
      }
      throw new Error(config.locale.auth.not_authorized);
    } catch (error) {
      throw new Error(error);
    }
  },
  updateLinkTitle: async (_, { data: { id, title } }, { db, authUser }) => {
    try {
      check.Auth(authUser);
      const user = await getUserFromLink(id);
      if (authUser.id === user.id) {

        const link = await db.links.findOne({
          where : { id: id }
        });
        await link.update({
          title : title
        });
  
        link.user = authUser.get({plain:true});
        return link;
      }
      throw new Error(config.locale.auth.not_authorized);
    } catch (error) {
      throw new Error(error);
    }
  },

  updateLinkOrder: async (_, { data: { id, order } }, { db, authUser }) => {
    try {
      check.Auth(authUser);
      const user = await getUserFromLink(id);
      if (authUser.id === user.id) {
        return await db.links.update({ order }, { where: { id: id } });
      }
      throw new Error(config.locale.auth.not_authorized);
    } catch (error) {
      throw new Error(error);
    }
  },

  deleteLink: async (_, { data: { id } }, { db, authUser }) => {
    try {
      check.Auth(authUser);
      const user = await getUserFromLink(id);
      if (authUser.id === user.id) {
        return await db.links.destroy({ where: { id: id } });
      }
      throw new Error(config.locale.auth.not_authorized);
    } catch (error) {
      throw new Error(error);
    }
  },

  addTag: async (_, { data: { id, tags } }, { db, authUser }) => {
    try {
      check.Auth(authUser);
      const user = await getUserFromLink(id);
      if (authUser.id === user.id) {

        const link = await db.links.findOne({
          where : { id: id }
        });

        tags = tags.map( ({ title }) => {
          return db.tags.findOrCreate({
            where : { title }
          })  
        })

        tags = await Promise.all(tags);
        
        tags = tags.map(response => response[0]);
        await link.addTags(tags);

        return tags;
        
        
      }
      throw new Error(config.locale.auth.not_authorized);
    } catch (error) {
      throw new Error(error);
    }
  },

  removeTag: async (_, { data: { id, tags } }, { db, authUser }) => {
    try {
      check.Auth(authUser);
      const user = await getUserFromLink(id);
      if (authUser.id === user.id) {
      
        return await db.link_tags.destroy({
          where : {
            tag_id : tags.map(t => t.id),
            link_id : id
          }
        })

       
      }
      throw new Error(config.locale.auth.not_authorized);
    } catch (error) {
      throw new Error(error);
    }
  }

};
