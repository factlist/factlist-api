const env = process.env.NODE_ENV || "development"
const config = {
	development: {
		username: "root",
		password: "",
		logging: false,
		database: "factlist-api",
		host: "localhost",
		dialect: "mysql",
		timezone: "+00:00",
		define: {
			paranoid: true,
			timestamps: true,
			freezeTableName: true,
			underscored: true
		},
		server: {
			port: process.env.port || 4000
		},
		auth: {
			jwtSecret: "secretKey"
		}
	},

	test: {
		username: "root",
		password: "",
		logging: false,
		database: "factlist-api",
		host: "localhost",
		dialect: "mysql",
		timezone: "+00:00",
		define: {
			paranoid: true,
			timestamps: true,
			freezeTableName: true,
			underscored: true
		},
		server: {
			port: process.env.port || 4000
		},
		auth: {
			jwtSecret: "secretKey"
		}
	},

	production: {
		username: "root",
		password: "",
		logging: false,
		database: "factlist-api",
		host: process.env.DB_HOST,
		dialect: "mysql",
		timezone: "+00:00",
		define: {
			paranoid: true,
			timestamps: true,
			freezeTableName: true,
			underscored: true
		},
		server: {
			port: process.env.port || 4000
		},
		auth: {
			jwtSecret: "secretKey"
		}
	}
}

module.exports = config[env]
