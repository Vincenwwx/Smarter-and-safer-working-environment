import gin


def main(argv):
    # Gin-configs
    gin.parse_config_files(['configs/configs.gin'])


if __name__ == "__main__":
    main()